interface UserDetails {
  email: string
  // JWT token
  token: string
}

const getStorageName = (prop: any) => `user-detail-${prop}`

export const setUserDetails = (data: Partial<UserDetails>) => {
  Object.keys(data).forEach((prop) => {
    // @ts-expect-error
    localStorage.setItem(getStorageName(prop), data[prop])

    // @ts-expect-error
    console.log(`Saved User Detail (${prop}) = ${data[prop]}`)
  })
}

export const getUserDetail = (detail: keyof UserDetails) => {
  return localStorage.getItem(getStorageName(detail))
}
