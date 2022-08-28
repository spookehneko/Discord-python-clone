import type { NextPage } from 'next'
import Head from 'next/head'
import Image from 'next/image'
import Link from 'next/link'

const DiscordLogo = () => {
  return (
    <div className='relative mt-10'>
      <img src={'/discord-logo.svg'} alt='Discord Logo' />
    </div>
  )
}

const LoginBtn = () => {
  return (
    <>
      <Link href={'/login'}>
        <button className='bg-discord-grey text-white rounded-lg py-2'>
          Login
        </button>
      </Link>
    </>
  )
}

const RegisterBtn = () => {
  return (
    <>
      <Link href={'/register'}>
        <button className='bg-discord-blue text-white rounded-lg py-2'>
          Register
        </button>
      </Link>
    </>
  )
}

const Home: NextPage = () => {
  return (
    <div className='w-screen h-screen flex items-center flex-col justify-between'>
      <DiscordLogo />

      <div className='flex flex-col justify-center items-center text-sm mb-5 gap-5'>
        <div className='text-center'>
          <div className='text-3xl whitespace-nowrap font-bold'>
            Welcome to Discord
          </div>
          <div className='text-discord-text-light text-center text-xs px-2'>
            Join over 100 million people who use Discord to talk with
            communities and friends
          </div>
        </div>

        <div className='flex flex-col w-56 gap-2'>
          <RegisterBtn />
          <LoginBtn />
        </div>
      </div>
    </div>
  )
}

export default Home
