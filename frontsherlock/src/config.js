export const getHeader = function () {
  const tokenData = JSON.parse(window.localStorage.getItem('authUser'))
  const headers = {
    Accept: 'application/json',
    Authorization: 'Basic ' + btoa(tokenData.token + ':')
  }
  return headers
}
