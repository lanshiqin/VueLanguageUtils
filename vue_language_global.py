#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

__author__ = '蓝士钦'


# 获取指定文件后缀
def get_file_extension(filename):
    arr = os.path.splitext(filename)
    return arr[len(arr) - 1]


# 获取指定目录下指定后缀的文件全路径名，返回数组
def get_file_path_list(path, find_suffix_array):
    s = []
    # 遍历路径下的所有文件夹
    for dirpath, dirnames, filenames in os.walk(path):
        # 遍历文件夹下的所有文件
        for filepath in filenames:
            # 匹配目标文件后缀
            for find_suffix in find_suffix_array:
                if get_file_extension(filepath) == find_suffix:
                    s.append(os.path.join(dirpath, filepath))
                    print(os.path.join(dirpath, filepath))
    return s


# 读取文件,根据匹配规则查找目标，输出到指定文件
def read_file_match_out(match_rule, exclude_rule, file_path_list, write_file):
    out_file = open(write_file, "w")
    for file_obj in file_path_list:
        file_obj_temp = ''
        file = open(file_obj, 'r', encoding='UTF-8')
        line = file.readline()
        while line:
            text_list = text_split_list(match_rule, exclude_rule, line)
            if not text_list:
                file_obj_temp += line
                line = file.readline()
                continue
            else:
                # 按字符长度倒叙排序
                text_list.sort(key=lambda x: len(x), reverse=True)
                for text in text_list:
                    if os.path.splitext(file_obj)[1] == '.html':
                        line = line.replace(text, '{{ $t("' + text + '") }}')
                        # line = re.sub('^(?!/\(".*/).*$' + text, '{{ $t("' + text + '") }}', line)
                    if os.path.splitext(file_obj)[1] == '.js':
                        line = line.replace('"' + text + '"', 'this.$t("' + text + '")')
                        line = line.replace("'" + text + "'", 'this.$t("' + text + '")')

                    out_file.write(text + '\n')
                    out_file.flush()
                file_obj_temp += line
            line = file.readline()
        file.close()
        file_write = open(file_obj, 'w', encoding='UTF-8')
        file_write.write(file_obj_temp)
        file_write.close()
    out_file.close()


# 根据规则查找出目标文字，返回数组
def text_split_list(match_rule, exclude_rule, text_str):
    for exr in exclude_rule:
        text_str = re.sub(exr, "", text_str)
    array_list = match_rule.split(text_str)
    while '' in array_list:
        array_list.remove('')
    return array_list


# 根据源文件生成多语言目标js文件
def generate_language_js_files(file_input, object_path, file_output_list):
    for file_output in file_output_list:
        file_out = open(object_path + '/' + file_output + '.js', 'w', encoding='UTF-8')
        file_out.write('const ' + file_output + ' = {\n')
        file = open(file_input, 'r')
        line = file.readline()
        while line:
            line = line.replace("\n", "")
            file_out.write("\t" + line + ": '" + line + "',\n")
            line = file.readline()
        file_out.write("}")
        file.close()
        file_out.close()


# 去重
def file_content_trim(write_file):
    content_temp = []
    file = open(write_file, 'r', encoding='gbk')
    line = file.readline()
    print('开始去重...')
    while line:
        if line in content_temp:
            line = file.readline()
            continue
        else:
            content_temp.append(line)
            line = file.readline()
    print('开始排序...')
    out_file = open(write_file, "w")
    # 按字符长度倒叙排序
    content_temp.sort(key=lambda x: len(x), reverse=True)
    for text in content_temp:
        out_file.write(text)
    out_file.close()
    file.close()
    print('提取完成')


# 根据实际情况
if __name__ == '__main__':
    # 项目路径
    project_path = 'F:/statics'

    # 要匹配的文件路径和文件后缀
    file_input_path = project_path
    find_suffix_list = ['.html', '.js']
    file_input_list = get_file_path_list(file_input_path, find_suffix_list)
    # 要匹配的规则
    match_re = re.compile('[^\u4E00-\u9FA5]')
    # 要排除的规则数组 排除html中的<!-- 和 // 注释
    exclude_re = [r'<!--.*$', r'//.*$', r'$t\(.*$']
    # 匹配到的值要输出到的指定文件
    source_file_path = project_path + '/zh_cn.txt'
    # 匹配输出
    read_file_match_out(match_re, exclude_re, file_input_list, source_file_path)

    # # 文件内容去重,排序
    file_content_trim(source_file_path)

    # 要输出的目标语种文件文件
    output_file_list = ['cn', 'am']
    # 生成多语言目标文件
    generate_language_js_files(source_file_path, project_path, output_file_list)

    print('国际化完成!')
