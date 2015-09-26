# -*- coding: utf-8 -*-
"""
That module is for generating web navigator's User-Agent header.

TODO:
* add Edge/IE
* You can build completely random user-agent or limit generation
to specific OS, browser, etc.
"""
from random import choice
import six

__all__ = ['generate_user_agent', 'generate_navigator']

PLATFORM = ('linux', 'mac', 'win')
NAVIGATOR = ('firefox', 'chrome')
APPVERSION = '5.0'
FIREFOX_USERAGENT_TEMPLATE = (
    'Mozilla/5.0 (%(platform)s; rv:%(version)s) '
    'Gecko/%(geckotrail)s Firefox/%(version)s'
)
CHROME_USERAGENT_TEMPLATE = (
    'Mozilla/5.0 (%(platform)s) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/%(version)s Safari/537.36'
)
WINDOWS_PLATFORM = (
    'Windows NT 5.1', # Windows XP
    'Windows NT 6.1', # Windows 7
    'Windows NT 6.2', # Windows 8
    'Windows NT 6.3', # Windows 8.1
    'Windows NT 10.0', # Windows 10
)
WINDOWS_SUBPLATFORM = (
    ('', 'Win32'), # 32bit
    ('Win64; x64', 'Win32'), # 64bit
    ('WOW64', 'Win32'), # 32bit process / 64bit system
)
MAC_PLATFORM = (
    'Macintosh; Intel Mac OS X 10.8',
    'Macintosh; Intel Mac OS X 10.9',
    'Macintosh; Intel Mac OS X 10.10',
    'Macintosh; Intel Mac OS X 10.11',
)
MAC_SUBPLATFORM = 'MacIntel' # 32bit, 64bit
LINUX_PLATFORM = (
    'X11; Linux',
    'X11; Ubuntu; Linux',
)
LINUX_SUBPLATFORM = (
    ('i686', 'Linux i686'), # 32bit
    ('x86_64', 'Linux x86_64'), # 64bit
    ('i686 on x86_64', 'Linux i686 on x86_64'), # 32bit process / 64bit system
)
FIREFOX_VERSION = (
#    '16.0','18.0','19.0','21.0','22.0','23.0','24.0','25.0',
    '27.0','28.0','29.0','31.0','33.0','36.0','37.0', '38.0',
    '39.0','40.0','41.0','42.0','43.0',
)
GECKOTRAIL_DESKTOP = '20100101'
CHROME_VERSION = (
#    '27.0.1453.116','27.0.1453.90','27.0.1453.93','27.0.1500.55',
#    '28.0.1464.0','28.0.1467.0','28.0.1468.0','29.0.1547.2','29.0.1547.57',
#    '29.0.1547.62','30.0.1599.17','31.0.1623.0','31.0.1650.16','32.0.1664.3',
#    '32.0.1667.0','33.0.1750.517','34.0.1847.116','34.0.1847.137','34.0.1866.237',
    '35.0.1916.47','35.0.2117.157','35.0.2309.372','35.0.3319.102','36.0.1944.0',
    '36.0.1985.125','36.0.1985.67','37.0.2049.0','37.0.2062.124','41.0.2224.3',
    '41.0.2225.0','41.0.2226.0','41.0.2227.1','41.0.2228.0','41.0.2272.76',
    '42.0.2311.1', '43.0.2357.134', '44.0.2403.130', '45.0.2454.85',
)


def generate_navigator(platform=None):
    """
    Generates navigator's config
    """
    if isinstance(platform, six.string_types):
        platform_name = platform
    elif isinstance(platform, (list, tuple)):
        platform_name = choice(platform)
    elif platform is None:
        platform_name = choice(PLATFORM)
    else:
        raise Exception('Option platform has invalid value: %s' % platform)

    if platform_name == 'win':
        subplatform, navigator_platform = choice(WINDOWS_SUBPLATFORM)
        win_platform = choice(WINDOWS_PLATFORM)
        if subplatform:
            platform = win_platform + '; ' + subplatform
        else:
            platform = win_platform
        oscpu = platform
    elif platform_name == 'linux':
        subplatform, navigator_platform = choice(LINUX_SUBPLATFORM)
        platform = choice(LINUX_PLATFORM) + ' ' + subplatform
        oscpu = navigator_platform
    elif platform_name == 'mac':
        navigator_platform = MAC_SUBPLATFORM
        platform = choice(MAC_PLATFORM)
        oscpu = platform[11:]
    if platform_name == 'mac':
        navigator_name = 'firefox'
    else:
        navigator_name = choice(NAVIGATOR)
    navigator_version = (
        choice(FIREFOX_VERSION)
        if navigator_name == 'firefox' else
        choice(CHROME_VERSION)
    )
    if navigator_name == 'firefox':
        user_agent = FIREFOX_USERAGENT_TEMPLATE % {
            'platform': platform,
            'version': navigator_version,
            'geckotrail': GECKOTRAIL_DESKTOP,
        }
    elif navigator_name == 'chrome':
        user_agent = CHROME_USERAGENT_TEMPLATE % {
            'platform': platform,
            'version': navigator_version,
        }
    return {
        'name': navigator_name,
        'version': navigator_version,
        'os': platform_name,
        'platform': navigator_platform,
        'oscpu': oscpu,
        'user_agent': user_agent,
        'appversion': APPVERSION,
    }


def generate_user_agent(**kwargs):
    """Generates HTTP User-Agent header"""
    return generate_navigator(**kwargs)['user_agent']
