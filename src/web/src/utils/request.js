import axios from 'axios'
import { Message } from 'element-ui'
import { getCSRF } from '@/utils/auth'

// 创建axios实例
const service = axios.create({
  timeout: 5000 // 请求超时时间
})

// request拦截器
service.interceptors.request.use(
  config => {
    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
      return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method)
    }
    if (!csrfSafeMethod(config.method)) {
      config.headers['X-CSRFToken'] = getCSRF()
    }
    return config
  },
  error => {
    // Do something with request error
    console.log(error) // for debug
    Promise.reject(error)
  }
)

// response 拦截器
service.interceptors.response.use(
  response => {
    const res = response
    if (res.status >= 500) {
      Message({
        message: res.data,
        type: 'error',
        duration: 5 * 1000
      })
      return Promise.reject('error')
    } else if (res.status === 401) {
      return Promise.reject('认证失败，请重新登陆。')
    } else if (res.status === 403) {
      return Promise.reject('您无权访问该接口。')
    } else {
      return response.data
    }
  },
  error => {
    console.log('err' + error) // for debug
    return Promise.reject(error)
  }
)

export default service
