import "@/styles/globals.css";
import { Inter } from "@next/font/google";
import type { AppProps } from "next/app";

import { RecoilRoot } from 'recoil'
import { AuthProvider } from '../hooks/useAuth'

export default function App({ Component, pageProps }: AppProps<{}>) {
  return (
        <AuthProvider>
            <RecoilRoot>
                <Component {...pageProps} />
            </RecoilRoot>
        </AuthProvider>
  );
}
