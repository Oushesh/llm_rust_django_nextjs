//Not use right but this one is for the OTPModal tool
import React, { useState } from 'react'
import {useRecoilState} from 'recoil';
import {modalState} from '../atoms/modalAtom';
import MuiModal from '@mui/material/Modal'
import XIcon from '@heroicons/react/outline/XIcon';
import toast, { Toaster } from 'react-hot-toast'
import { useForm, SubmitHandler } from 'react-hook-form'
import axios from 'axios';
interface Inputs
{
  email: string
  password: string
}

function OPTModal()
{
    const [showModal,setShowModal] = useRecoilState(modalState);
    const [clickPosition,setClickPosition] = useState({x:0,y:0});

    const [gmail,setGmail] = useState('');
    const [password,setPassword] = useState('');

    const handleGmailChange = (event:any) => {
      setGmail(event.target.value);
    };

    const handlePasswordChange = (event:any) => {
      setPassword(event.target.value);
    };

    const handleClose = () =>
    {
        setShowModal(false);
        toast.dismiss;
    }

    const centerScreen =
    {
        x: window.innerWidth / 2,
        y: window.innerHeight / 2
    };


    const {
      register,
      handleSubmit,
      watch,
      formState: { errors }
    } = useForm<Inputs>()


const onSubmit: SubmitHandler<Inputs> = async (data) => {
    try {
        const credentials = btoa('oushesh:1qay3edc5tgb7ujm');
        const response = await axios.post("http://127.0.0.1:8000/api/confirm_otp/otp_verification?email=oushesh&password=1qay3edc5tgb7ujm&OTP=`${data.password}`")

        console.log('Successful login');
    } catch (error) {
        console.error('Login failed:', error);
    }
};
      return (
        <div className={showModal ? "fixed inset-0 flex items-center justify-center z-50" : "hidden"}>
        <MuiModal
          open={showModal}
          onClose={handleClose}
          className="mx-auto w-full max-w-5xl overflow-hidden overflow-y-scroll scrollbar-hide rounded-l-3xl rounded-r-3xl"
        >
          <div className="bg-zinc bg-opacity-100 flex flex-items flex-col">
          <Toaster position="bottom-center" />
          <button
            className="modalButton absolute right-5 top-5 !z-40 h-9 w-9 border-none bg-[#181818] hover:bg-[#181818]"
            onClick={handleClose}
          >
            <XIcon className="h-6 w-6" />
          </button>
          <form
          className="relative mt-24 space-y-8 rounded bg-black/75 py-10 px-6 md:mt-0 md:max-w-md md:px-14
          rounded-l-3xl rounded-r-3xl"
          onSubmit={handleSubmit(onSubmit)}
          >
                <h1 className="text-4xl font-semibold">
                  2Factor Auth
                </h1>

                <div className="space-y-4">
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
                    onClick={() => setShowModal(true)}
                    type="submit"
                >
                    Confirm OTP
                </button>
            </form>

          </div>
        </MuiModal>
        </div>
      );
    };

<<<<<<< HEAD
export default OPTModal;
=======
export default OPTModal;
>>>>>>> Frontend_Debug
