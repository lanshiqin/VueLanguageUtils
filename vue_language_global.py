import os
import re

__author__ = '蓝士钦'


# 获取指定目录下指定后缀的文件全路径名，返回数组
def get_file_path_list(path, find_suffix):
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    s = []
    for file in files:  # 遍历文件夹
        if os.path.splitext(file)[1] == find_suffix:
            s.append(path + "/" + file)
    return s


# 读取文件,根据匹配规则查找目标，输出到指定文件
def read_file_match_out(match_rule, exclude_rule, file_path_list, write_file):
    out_file = open(write_file, "w")
    for file_obj in file_path_list:
        file = open(file_obj, 'r')
        line = file.readline()
        while line:
            text_list = text_split_list(match_rule, exclude_rule, line)
            if not text_list:
                pass
            else:
                for text in text_list:
                    out_file.write(text + '\n')
            line = file.readline()
        file.close()
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
        file_out = open(object_path + '/' + file_output + '.js', 'w')
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


# 按行读取文件内容转换成数组
def read_file_to_list(file_input):
    file = open(file_input, 'r')
    line = file.readline()
    file_list = []
    while line:
        line = line.replace('\n', '')
        file_list.append(line)
        line = file.readline()
    return file_list


# 根据中文键名称替换目标文件集合中的中文为VueI18n的模板表达式
def replace_I18n_template(key_list, file_path_list):
    for file_obj in file_path_list:
        file_obj_temp = ''
        for key in key_list:
            file = open(file_obj, 'r')
            line = file.readline()
            while line:
                line = line.replace(key, '{{ $t("' + key + '") }}')
                file_obj_temp += line
                line = file.readline()
            file.close()
            file_write = open(file_obj, 'w')
            file_write.write(file_obj_temp)
            file_obj_temp = ''
            file_write.close()


# 根据实际情况
if __name__ == '__main__':
    # 项目路径
    project_path = '/Users/lanshiqin/Temp/vue-demo'

    # 要匹配的文件路径和文件后缀
    file_input_path = project_path
    file_input_list = get_file_path_list(file_input_path, '.html')
    # 要匹配的规则
    match_re = re.compile('[^\u4E00-\u9FA5]')
    # 要排除的规则数组 排除html中的<!-- 和 // 注释
    exclude_re = [r'<!--.*$', r'//.*$']
    # 匹配到的值要输出到的指定文件
    source_file_path = project_path + '/zh_cn.txt'
    # 匹配输出
    read_file_match_out(match_re, exclude_re, file_input_list, source_file_path)

    # 要输出的目标语种文件文件
    output_file_list = ['cn', 'en']
    # 生成多语言目标文件
    generate_language_js_files(source_file_path, project_path, output_file_list)

    # 读取指定文件包装成数组
    file_key_list = read_file_to_list(source_file_path)
    # 对匹配的文件进行VueI18n模板表达式替换
    replace_I18n_template(file_key_list, file_input_list)

    print('国际化完成')
