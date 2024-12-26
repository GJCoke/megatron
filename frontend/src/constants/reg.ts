// 用户名正则：4到16个字符，包括中英文字符、字母、数字、下划线和破折号
export const REG_USER_NAME = /^[\u4E00-\u9FA5a-zA-Z0-9_-]{4,16}$/

/** 电话号码正则： 以1开头，后跟特定的数字组合，共11位 */
export const REG_PHONE =
  /^[1](([3][0-9])|([4][01456789])|([5][012356789])|([6][2567])|([7][0-8])|([8][0-9])|([9][012356789]))[0-9]{8}$/

/** 密码正则： 6到18个字符，包括字母、数字和下划线 */
export const REG_PWD = /^[a-zA-Z0-9]{6,18}$/

/** 邮箱正则： 标准邮箱格式，包括字母、数字、下划线和各种符号 */
export const REG_EMAIL = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/

/** 六位数字验证码正则 */
export const REG_CODE_SIX = /^\d{6}$/

/** 四位数字验证码正则 */
export const REG_CODE_FOUR = /^\d{4}$/

/** URL正则： 匹配标准的 URL 格式 */
export const REG_URL =
  /(((^https?:(?:\/\/)?)(?:[-;:&=+$,\w]+@)?[A-Za-z0-9.-]+(?::\d+)?|(?:www.|[-;:&=+$,\w]+@)[A-Za-z0-9.-]+)((?:\/[+~%/.\w-_]*)?\??(?:[-+=&;%@.\w_]*)#?(?:[\w]*))?)$/