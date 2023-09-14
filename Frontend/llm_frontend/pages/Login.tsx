//Login Page shown before the user puts in the credentials and signs in the app
import Head from 'next/head'
import Image from 'next/image'
import {useRef, useState} from 'react'
import {useForm, SubmitHandler} from 'react-hook-form'
import useAuth from '../hooks/useAuth'

import {useRecoilState,useRecoilValue} from 'recoil';
import {modalState,OTPmodalState} from '../atoms/modalAtom'
import React from 'react';

function Login() {
    const [login, setLogin] = useState(false)
    const {signIn,signUp} = useAuth()

    const [showModal,setShowModal] = useRecoilState()

    const {
        register,
        handleSubmit,
        watch,
        formstate: {errors},
    } = useForm<inpus>()

    //The JSX Component for the page
    return (
        <div className="relative flex h-screen w-screen flex-col md:items-center md:justify-center">
            <Head>
                <title>Netflix</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>
            <form
                className="relative mt-24 space-y-8 rounded bg-black/75 py-10 px-6 md:mt-0 md:max-w-md md:px-14 rounded-l-3xl rounded-r-3xl"
                onSubmit={handleSubmit(onSubmit)}
            >
                <h1 className="text-4xl font-semibold">Sign In</h1>
                <div className="space-y-4">
                    <label className="inline-block w-full">
                        <input
                            type="email"
                            placeholder="Email"
                            className="input"
                            {...register('email', { required: true })}
                        />
                        {errors.email && (
                            <p className="text-sm  text-orange-500">
                                Please enter a valid email.
                            </p>
                        )}
                    </label>
                    <label className="inline-block w-full">
                        <input
                            type="password"
                            {...register('password', { required: true })}
                            placeholder="Password"
                            className="input"
                        />
                        {errors.password && (
                            <p className="text-sm text-orange-500">
                                Your password must contain between 4 and 60 characters.
                            </p>
                        )}
                    </label>
                </div>
                <button
                    className="w-full rounded bg-[#075985] py-3 font-semibold"
                    onClick={() => setLogin(true)}
                    type="submit"
                >
                    Sign In
                </button>
                <button
                    className="w-full rounded bg-[#075985] py-3 font-semibold"
                    onClick={() => setShowModal(true)}
                    type="button"
                >
                    2FactorAuthentication
                </button>

            </form>
            {/*Wrap this component out and finish the 2Factor Model */}
            {showModal &&  <OTP/>}
        </div>
    )

}

export default Login