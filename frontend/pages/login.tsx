import styles from '@styles/Login.module.css'
import Link from 'next/link'
import { useFormik } from 'formik'
import { setUserDetails, getUserDetail } from '@libs/user'
import * as URL from '@libs/urls'
import { useEffect } from 'react'
import { useRouter } from 'next/router'
import axios from 'axios'

interface LoginFormFields {
  email: string
  password: string
}

const useLogin = () => {
  const router = useRouter()

  const formik = useFormik<LoginFormFields>({
    initialValues: {
      email: '',
      password: '',
    },
    onSubmit: async (values, formikHelpers) => {
      // CONTACT TO SERVER & GET TOKEN

      const res = await axios.post(URL.LOGIN, values)

      if (res?.data?.message) alert(res?.data?.message)

      setUserDetails({
        email: values.email,
      })

      router.push('/protected/home')
    },
  })

  return [formik] as const
}

const Login = () => {
  const [formik] = useLogin()

  useEffect(() => {
    console.log('LocalStorage User : ', getUserDetail('email'))
  }, [])

  return (
    <>
      <div className='mt-12'>
        <div className='text-center mb-10'>
          <div className='text-2xl'>Welcome back!</div>
          <div className='text-discord-text-light text-sm'>
            Log in with your email to start chatting.
          </div>
        </div>
        <form onSubmit={formik.handleSubmit}>
          <div className='flex flex-col px-2'>
            <div className='uppercase font-bold text-xs mb-1'>
              ACCOUNT INFORMATION
            </div>
            <div className='formInputs flex flex-col gap-3'>
              <div className='rounded-md bg-discord-dark py-3 px-4 w-full'>
                <input
                  onChange={formik.handleChange}
                  value={formik.values.email}
                  className={`formInp`}
                  type='email'
                  name='email'
                  placeholder='email'
                />
              </div>
              <div className='rounded-md bg-discord-dark py-3 px-4 w-full'>
                <input
                  onChange={formik.handleChange}
                  value={formik.values.password}
                  className={`formInp`}
                  type='password'
                  name='password'
                  placeholder='Password'
                />
              </div>
            </div>

            {/* <div className='text-discord-glow-blue text-sm'>
              Forget your password?
            </div> */}
            <div className='w-full mt-8'>
              <input
                disabled={formik.isSubmitting}
                value='Login'
                type='submit'
                className='bg-discord-blue text-white rounded-lg py-2 w-full '
              />
            </div>
          </div>
        </form>
      </div>
    </>
  )
}

export default Login
