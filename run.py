#!/usr/bin/python3

'''
# @Author       : Chr_
# @Date         : 2020-07-14 16:36:33
# @LastEditors  : Chr_
# @LastEditTime : 2020-09-05 00:14:20
# @Description  : 启动入口
'''

import os
import sys
import time
import traceback


try:
    from utils.config import load_config
    from utils.log import get_logger
    from utils.ftqq import send_to_ftqq
    from utils.email import send_to_email
    from utils import cliwait
    from utils.version import check_script_update
    from utils.version import SCRIPT_VERSION

    from pojie52.SignIn52pj import variable_52pj
    from pojie52.SignIn52pj import conventional_52pj


except ImportError as e:
    print(e)
    print('导入模块出错,请执行 pip install -r requirements.txt 安装所需的依赖库')
    cliwait()
    exit()


logger = get_logger('Run')


def conventional():

    pojie52 = CFG['52pojie']
    mcfg = CFG['main']
    ftqq = CFG['ftqq']

    conventional_52pj(pojie52,ftqq['skey'])

    data = []
    logger.info(f'脚本版本:[{SCRIPT_VERSION}]')
    data.append(f'#### {"=" * 30 }\n'
                f'#### 脚本版本:[{SCRIPT_VERSION}]')

    end_time = time.time()
    logger.info(f'脚本耗时:[{round(end_time-start_time,4)}]s')
    data.append(f'#### 任务耗时:[{round(end_time-start_time,4)}]s')

    message = '\n'.join(data)

    title = '自动签到脚本'
    if mcfg['check_update']:
        logger.info('检查脚本更新……')
        result = check_script_update()
        if result:
            latest_version, detail, download_url = result
            logger.info(f'-->脚本有更新<--'
                        f'最新版本[{latest_version}]'
                        f'更新内容[{detail}]'
                        f'下载地址[{download_url}]')
            data.append('')
            data.append = (f'### 脚本有更新\n'
                           f'#### 最新版本[{latest_version}]\n'
                           f'#### 下载地址:[GitHub]({download_url})\n'
                           f'#### 更新内容\n'
                           f'{detail}\n'
                           f'> 如果碰到问题欢迎联系QQ**814046228**')
            title += '【有更新】'
        else:
            logger.info(f'脚本已是最新,当前版本{SCRIPT_VERSION}')
    else:
        logger.info(f'检查脚本更新已禁用,当前版本{SCRIPT_VERSION}')

    logger.info('推送统计信息……')
    message_push(title, message, True)
    logger.info('脚本执行完毕')


def variable():
    SCKEY = os.environ.get('SCKEY')
    mcfg = CFG['main']
    data = []

    cookie_52pj = os.environ.get('cookie_52pj')

    variable_52pj(cookie_52pj,SCKEY)

    end_time = time.time()
    logger.info(f'脚本耗时:[{round(end_time-start_time,4)}]s')
    data.append(f'#### 任务耗时:[{round(end_time-start_time,4)}]s')

    message = '\n'.join(data)

    title = '自动签到脚本'
    if mcfg['check_update']:
        logger.info('检查脚本更新……')
        result = check_script_update()
        if result:
            latest_version, detail, download_url = result
            logger.info(f'-->脚本有更新<--'
                        f'最新版本[{latest_version}]'
                        f'更新内容[{detail}]'
                        f'下载地址[{download_url}]')
            data.append('')
            data.append = (f'### 脚本有更新\n'
                           f'#### 最新版本[{latest_version}]\n'
                           f'#### 下载地址:[GitHub]({download_url})\n'
                           f'#### 更新内容\n'
                           f'{detail}\n'
                           f'> 如果碰到问题欢迎加QQ**814046228**')
            title += '【有更新】'
        else:
            logger.info(f'脚本已是最新,当前版本{SCRIPT_VERSION}')
    else:
        logger.info('检查脚本更新已禁用,当前版本{SCRIPT_VERSION}')

    logger.info('推送统计信息……')
    message_push(title, message, True)
    logger.info('脚本执行完毕')


def message_push(title: str, message: str, error: bool = False):
    '''
    推送通知
    '''
    ftqq = CFG['ftqq']
    email = CFG['email']
    if ftqq['enable']:
        if (ftqq['only_on_error'] == True and error) or (ftqq['only_on_error'] == False):
            result = send_to_ftqq(title, message, ftqq)
            if result:
                logger.info('FTQQ推送成功')
            else:
                logger.warning('[*] FTQQ推送失败')
    if email['enable']:
        if (email['only_on_error'] == True and error) or (email['only_on_error'] == False):
            result = send_to_email(title, message, email)
            if result:
                logger.info('邮件推送成功')
            else:
                logger.warning('[*] 邮件推送失败')


if __name__ == '__main__':
    run_type = sys.argv[1]
    start_time = time.time()

    if "1" in run_type:
        try:
            logger.info('载入配置文件')
            CFG = load_config()
        except FileNotFoundError:
            logger.error('[*] 配置文件[config.toml]不存在,请参考[README.md]生成配置')
            cliwait()
        except ValueError:
            logger.error('[*] 尚未配置有效的账户凭据,请添加到[config.toml]中')
            cliwait()
        except Exception as e:
            logger.error(f'[*] 载入配置文件出错,请检查[config.toml] [{e}]')
            cliwait()
            exit()

        try:
            conventional()
        except KeyboardInterrupt:
            logger.info('[*] 手动终止运行')
            cliwait()
        except Exception as e:
            logger.error(f'遇到未知错误 [{e}]', exc_info=True)
            title = '脚本执行遇到未知错误'
            message = (f'#### 脚本版本:[{SCRIPT_VERSION}]\n'
                       f'#### 系统信息:[{os.name}]\n'
                       f'#### Python版本: [{sys.version}]\n'
                       f'#### {"=" * 30}\n'
                       f'#### 错误信息: {traceback.format_exc()}\n'
                       f'#### {"=" * 30}\n'
                       '#### 联系信息:\n'
                       '* QQ: 814046228\n'
                       '* TG群: https://t.me/joinchat/HTtNrSJLz7s2A-0N\n'
                       '* 邮箱: admin@lyile.cn\n'
                       '> 如果需要帮助请附带上错误信息')
            message_push(title, message, True)
            cliwait()
    elif "2" in run_type:
        try:
            variable()
        except KeyboardInterrupt:
            logger.info('[*] 手动终止运行')
            cliwait()
        except Exception as e:
            logger.error(f'遇到未知错误 [{e}]', exc_info=True)
            title = '脚本执行遇到未知错误'
            message = (f'#### 脚本版本:[{SCRIPT_VERSION}]\n'
                       f'#### 系统信息:[{os.name}]\n'
                       f'#### Python版本: [{sys.version}]\n'
                       f'#### {"=" * 30}\n'
                       f'#### 错误信息: {traceback.format_exc()}\n'
                       f'#### {"=" * 30}\n'
                       '#### 联系信息:\n'
                       '* QQ: 814046228\n'
                       '* TG群: https://t.me/joinchat/HTtNrSJLz7s2A-0N\n'
                       '* 邮箱: admin@lyile.cn\n'
                       '> 如果需要帮助请附带上错误信息')
            message_push(title, message, True)
            cliwait()
    else:
        print('该启动方式不存在:', run_type)




