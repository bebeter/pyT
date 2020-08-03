#!/usr/bin/env python
#  -*- coding: utf-8 -*-

"""
作者：小黎
策略逻辑：
以监控表的形式监控网格策略，实现开仓后马上挂单平仓的动作。同时上下网格独立，实现网格随行情移动的自适应逻辑。
生于震荡，死于趋势。
本策略仅供参考，切勿实盘！

"""
#################################################################################

from tqsdk import TqApi
from tqsdk.tafunc import time_to_datetime
from datetime import datetime
import pandas as pd
import numpy as np
from functools import reduce

#################################################################################

api = TqApi(web_gui=True)
symbol = "SHFE.rb2010"
close = "CLOSETODAY"  # 平今方式
quote = api.get_quote(symbol)
ticks = api.get_tick_serial(symbol)
position = api.get_position(symbol)
GRID_AMOUNT = 10
grid_region_long = [1 * quote.price_tick] * GRID_AMOUNT  # 多头每格价格跌幅(网格密度)
grid_region_short = [1 * quote.price_tick] * GRID_AMOUNT  # 空头每格价格涨幅(网格密度)
grid_volume_long = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]  # 多头每格持仓手数
grid_volume_short = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]  # 空头每格持仓手数
profit_long = 1 * quote.price_tick  # 多头利润
profit_short = 1 * quote.price_tick  # 空头利润
is_clear_all1 = False
is_clear_all2 = False


#################################################################################

def reset_df_long(quote, GRID_AMOUNT, grid_region_long, grid_volume_long):
    """生成多头网格监控表"""

    grid_prices_long = [reduce(lambda p, r: p - r, grid_region_long[:i], quote.ask_price1) for i in
                        range(GRID_AMOUNT + 1)][1:]  # 多头每格的触发价位列表
    df_long = pd.DataFrame(data=float("nan"), index=range(len(grid_prices_long)),
                           columns=["合约", "方向", "价格", "目标持仓", "持仓", "委开", "委开单号", "委平", "委平单号"])
    df_long["价格"] = grid_prices_long
    df_long["合约"] = [symbol] * GRID_AMOUNT
    df_long["方向"] = ["BUY"] * GRID_AMOUNT
    df_long["目标持仓"] = grid_volume_long
    df_long["持仓"] = [0] * GRID_AMOUNT
    df_long["委开"] = [0] * GRID_AMOUNT
    df_long["委平"] = [0] * GRID_AMOUNT
    return df_long


def reset_df_short(quote, GRID_AMOUNT, grid_region_short, grid_volume_short):
    """生成空头网格监控表"""

    grid_prices_short = [reduce(lambda p, r: p + r, grid_region_short[:i], quote.bid_price1) for i in
                         range(GRID_AMOUNT + 1)][1:]  # 空头每格的触发价位列表
    df_short = pd.DataFrame(data=float("nan"), index=range(len(grid_prices_short)),
                            columns=["合约", "方向", "价格", "目标持仓", "持仓", "委开", "委开单号", "委平", "委平单号"])
    df_short["价格"] = grid_prices_short
    df_short["合约"] = [symbol] * GRID_AMOUNT
    df_short["方向"] = ["SELL"] * GRID_AMOUNT
    df_short["目标持仓"] = grid_volume_long
    df_short["持仓"] = [0] * GRID_AMOUNT
    df_short["委开"] = [0] * GRID_AMOUNT
    df_short["委平"] = [0] * GRID_AMOUNT
    return df_short


#################################################################################

df_long = reset_df_long(quote, GRID_AMOUNT, grid_region_long, grid_volume_long)
df_short = reset_df_short(quote, GRID_AMOUNT, grid_region_short, grid_volume_short)

#################################################################################

while True:

    api.wait_update()
    #################################################################################

    if api.is_changing(ticks):
        now = time_to_datetime(ticks.iloc[-1].datetime)
        if (now.hour >= 9 and now.hour < 15) or (now.hour >= 21 and now.hour < 23):

            if is_clear_all1:
                api.insert_order(symbol, "SELL", close, position.pos_long, quote.bid_price1 - 2)
                is_clear_all1 = False
            if is_clear_all2:
                api.insert_order(symbol, "BUY", close, position.pos_short, quote.ask_price1 + 2)
                is_clear_all2 = False

            #################################################################################

            if api.is_changing(quote):
                df = pd.DataFrame(api.get_order().values())
                if not df.empty:
                    df_long_open = df[
                        ((df["exchange_id"] + "." + df["instrument_id"]) == symbol) & (df["direction"] == "BUY") & (
                                    df["offset"] == "OPEN") & (df["volume_left"] == df["volume_orign"]) & (
                                    df["status"] == "ALIVE")]
                    df_short_open = df[
                        ((df["exchange_id"] + "." + df["instrument_id"]) == symbol) & (df["direction"] == "SELL") & (
                                    df["offset"] == "OPEN") & (df["volume_left"] == df["volume_orign"]) & (
                                    df["status"] == "ALIVE")]
                    df_long_close = df[
                        ((df["exchange_id"] + "." + df["instrument_id"]) == symbol) & (df["direction"] == "SELL") & (
                                    df["offset"] == close) & (df["volume_left"] == df["volume_orign"]) & (
                                    df["status"] == "ALIVE")]
                    df_short_close = df[
                        ((df["exchange_id"] + "." + df["instrument_id"]) == symbol) & (df["direction"] == "BUY") & (
                                    df["offset"] == close) & (df["volume_left"] == df["volume_orign"]) & (
                                    df["status"] == "ALIVE")]
                else:
                    df_long_open = pd.DataFrame()
                    df_short_open = pd.DataFrame()
                    df_long_close = pd.DataFrame()
                    df_short_close = pd.DataFrame()

                #################################################################################

                # 多头网格监控表
                for index, row in df_long.iterrows():
                    if row["持仓"] + row["委开"] < row["目标持仓"]:
                        order_open = api.insert_order(row["合约"], row["方向"], "OPEN", row["目标持仓"] - row["持仓"] - row["委开"],
                                                      row["价格"])
                        df_long.iloc[index, 5], df_long.iloc[index, 6] = row[
                                                                             "委开"] + order_open.volume_orign, order_open.order_id
                    if row["委开"] > 0 and row["委开单号"] != float("nan"):
                        order_open_info = api.get_order(row["委开单号"])
                        if order_open_info.status == "FINISHED" and order_open_info.volume_left == 0:
                            df_long.iloc[index, 4], df_long.iloc[index, 5], df_long.iloc[index, 6] = row[
                                                                                                         "持仓"] + order_open_info.volume_orign, \
                                                                                                     row[
                                                                                                         "委开"] - order_open_info.volume_orign, float(
                                "nan")
                    if row["委平"] < row["持仓"]:
                        order_close = api.insert_order(row["合约"], "SELL", close, row["持仓"], row["价格"] + profit_long)
                        df_long.iloc[index, 7], df_long.iloc[index, 8] = row[
                                                                             "委平"] + order_close.volume_orign, order_close.order_id
                    if row["委平"] > 0 and row["委平单号"] != float("nan"):
                        order_close_info = api.get_order(row["委平单号"])
                        if order_close_info.status == "FINISHED" and order_close_info.volume_left == 0:
                            df_long.iloc[index, 4], df_long.iloc[index, 7], df_long.iloc[index, 8] = row[
                                                                                                         "持仓"] - order_close_info.volume_orign, \
                                                                                                     row[
                                                                                                         "委平"] - order_close_info.volume_orign, float(
                                "nan")

                # 多头委托10分钟不成交撤单，重设网格
                if not df_long_open.empty and position.pos_long_today == 0:
                    if df_long_open.insert_date_time.max() > 0 and time_to_datetime(quote.datetime) > time_to_datetime(
                            df_long_open.insert_date_time.max()):
                        if (time_to_datetime(quote.datetime) - time_to_datetime(
                                df_long_open.insert_date_time.max())).seconds > 10 * 60:
                            for i in df_long_open.order_id:
                                api.cancel_order(i)
                            df_long = reset_df_long(quote, GRID_AMOUNT, grid_region_long, grid_volume_long)

                # 多头平仓10分钟无成交且价格偏离5跳以上，平仓且重设多头网格
                if not df_long_close.empty and position.pos_short_today > 0:
                    if df_long_close.insert_date_time.max() > 0 and time_to_datetime(quote.datetime) > time_to_datetime(
                            df_long_close.insert_date_time.max()):
                        if (time_to_datetime(quote.datetime) - time_to_datetime(
                                df_long_close.insert_date_time.max())).seconds > 10 * 60 and df_long_close.limit_price.min() - quote.bid_price1 >= 5:
                            for i in df_long_close.order_id:
                                api.cancel_order(i)
                            is_clear_all1 = True
                            df_long = reset_df_long(quote, GRID_AMOUNT, grid_region_long, grid_volume_long)

                #################################################################################

                # 空头网格监控表
                for index2, row2 in df_short.iterrows():
                    if row2["持仓"] + row2["委开"] < row2["目标持仓"]:
                        order_open = api.insert_order(row2["合约"], row2["方向"], "OPEN",
                                                      row2["目标持仓"] - row2["持仓"] - row2["委开"], row2["价格"])
                        df_short.iloc[index2, 5], df_short.iloc[index2, 6] = row2[
                                                                                 "委开"] + order_open.volume_orign, order_open.order_id
                    if row2["委开"] > 0 and row2["委开单号"] != float("nan"):
                        order_open_info = api.get_order(row2["委开单号"])
                        if order_open_info.status == "FINISHED" and order_open_info.volume_left == 0:
                            df_short.iloc[index2, 4], df_short.iloc[index2, 5], df_short.iloc[index2, 6] = row2[
                                                                                                               "持仓"] + order_open_info.volume_orign, \
                                                                                                           row2[
                                                                                                               "委开"] - order_open_info.volume_orign, float(
                                "nan")
                    if row2["委平"] < row2["持仓"]:
                        order_close = api.insert_order(row2["合约"], "BUY", close, row2["持仓"], row2["价格"] - profit_short)
                        df_short.iloc[index2, 7], df_short.iloc[index2, 8] = row2[
                                                                                 "委平"] + order_close.volume_orign, order_close.order_id
                    if row2["委平"] > 0 and row2["委平单号"] != float("nan"):
                        order_close_info = api.get_order(row2["委平单号"])
                        if order_close_info.status == "FINISHED" and order_close_info.volume_left == 0:
                            df_short.iloc[index2, 4], df_short.iloc[index2, 7], df_short.iloc[index2, 8] = row2[
                                                                                                               "持仓"] - order_close_info.volume_orign, \
                                                                                                           row2[
                                                                                                               "委平"] - order_close_info.volume_orign, float(
                                "nan")

                # 空头10分钟不成交撤单，重设网格
                if not df_short_open.empty and position.pos_short_today == 0:
                    if df_short_open.insert_date_time.max() > 0 and time_to_datetime(quote.datetime) > time_to_datetime(
                            df_short_open.insert_date_time.max()):
                        if (time_to_datetime(quote.datetime) - time_to_datetime(
                                df_short_open.insert_date_time.max())).seconds > 10 * 60:
                            for i in df_short_open.order_id:
                                api.cancel_order(i)
                            df_short = reset_df_short(quote, GRID_AMOUNT, grid_region_short, grid_volume_short)

                # 空头平仓10分钟无成交且价格偏离5跳以上，平仓且重设空头网格
                if not df_short_close.empty and position.pos_short_today > 0:
                    if df_short_close.insert_date_time.max() > 0 and time_to_datetime(
                            quote.datetime) > time_to_datetime(df_short_close.insert_date_time.max()):
                        if (time_to_datetime(quote.datetime) - time_to_datetime(
                                df_short_close.insert_date_time.max())).seconds > 10 * 60 and quote.ask_price1 - df_short_open.limit_price.max() > 5:
                            for i in df_short_close.order_id:
                                api.cancel_order(i)
                            is_clear_all2 = True
                            df_short = reset_df_short(quote, GRID_AMOUNT, grid_region_short, grid_volume_short)
