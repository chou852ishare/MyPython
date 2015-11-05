# -*- coding: UTF-8 -*-

__author__ = 'ziye'


import datetime
import json
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


now = datetime.datetime.now()
date = now.date().strftime('%Y-%m-%d')
root = '/home/ziye/MyPython/lenovo_appstore_crawl/'  # make sure if the path is correct in big001
path_json = root + 'json/'
path_feature = root + 'feature/'  # create feature folder
if not os.path.isdir(path_feature):
    os.mkdir(path_feature)

# 11 app ranking lists
prefix_tuple = ('app_new_', 'app_rank_', 'app_rise_',
                'game_free_', 'game_local_', 'game_network_', 'game_new_', 'game_pop_',
                'root_app_', 'root_game_', 'root_rank_')


def get_clean_value(dict0, key):
    # clean \r, \n, ',' in raw value
    return unicode(dict0[key]).replace('\r', '').replace('\n', '').replace(',', '#')


def combine_for_prefix(prefix, hour):
    feature = {}
    rank = 0
    for si in range(1, 1601, 200):
        filename = prefix + date + '_' + unicode(hour) + '_' + unicode(si) + '_' + unicode(si+200-1) + '.json'
        try:
            f = open(path_json+filename, 'r')
            app_list = json.load(f)['datalist']
            for app in app_list:
                rank += 1
                pne = get_clean_value(app, 'packageName')
                vsn = get_clean_value(app, 'version')
                vce = get_clean_value(app, 'versioncode')
                did = get_clean_value(app, 'developerId')
                asz = get_clean_value(app, 'apkSize')
                ast = get_clean_value(app, 'averageStar')
                dct = get_clean_value(app, 'downloadCount')
                sdc = get_clean_value(app, 'shortDesc')
                tii = get_clean_value(app, 'typeInfoId')
                tne = get_clean_value(app, 'typeName')
                ipy = get_clean_value(app, 'ispay')
                ipl = get_clean_value(app, 'isPrivilege')
                hay = get_clean_value(app, 'hasActivity')
                hgg = get_clean_value(app, 'hasGameGift')
                hsy = get_clean_value(app, 'hasStrategy')
                hip = get_clean_value(app, 'hasInnerPay')
                had = get_clean_value(app, 'hasAd')
                hqt = get_clean_value(app, 'highQualityTag')
                fst = get_clean_value(app, 'fState')
                hst = get_clean_value(app, 'hState')
                lst = get_clean_value(app, 'lState')
                ost = get_clean_value(app, 'oState')
                vst = get_clean_value(app, 'vState')
                bcg = get_clean_value(app, 'bigCategory')
                gct = get_clean_value(app, 'gradeCount')
                gid = get_clean_value(app, 'groupId')
                rk = unicode(rank)
                key = pne + ',' + vsn
                desc = ','.join([vce, did, asz, ast, dct, sdc, tii, tne, ipy, ipl, hay, hgg,
                                 hsy, hip, had, hqt, fst, hst, lst, ost, vst, bcg, gct, gid])
                feature[key] = [desc, rk]
        except IOError:
            pass
    return feature


def join_feature(feature_all, feature_pre, empty_rank):
    # join different ranks in feature_all
    for key in feature_pre.keys():
        if key in feature_all.keys():
            # combine ranks
            feature_all[key][1].append(feature_pre[key][1])
        else:
            # create description and insert empty previous ranks
            ranks = empty_rank[:]
            ranks.append(feature_pre[key][1])
            feature_all[key] = [feature_pre[key][0], ranks]
    for key in feature_all.keys():
        if key not in feature_pre.keys():
            # append empty rank at end
            feature_all[key][1].append('')
    return feature_all


def combine_for_hour(hour):
    feature_file = path_feature + '_'.join(['app_content', date, str(hour)]) + '.csv'
    feature_all = {}
    empty_rank = []
    for prefix in prefix_tuple:
        feature_pre = combine_for_prefix(prefix, hour)
        feature_all = join_feature(feature_all, feature_pre, empty_rank)
        empty_rank.append('')
    if os.path.exists(feature_file):
        os.remove(feature_file)
    with open(feature_file, 'a') as f:
        for key in feature_all.keys():
            f.write(','.join([key, feature_all[key][0], ','.join(feature_all[key][1])]) + '\n')


# combine for one day
for hour in range(24):
    combine_for_hour(hour)