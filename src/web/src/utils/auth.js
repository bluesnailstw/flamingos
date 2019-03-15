import Cookies from 'js-cookie'

const TokenKey = 'sessionid'
const CSRFKey = 'csrftoken'

export function getCSRF() {
  return Cookies.get(CSRFKey)
}

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}
