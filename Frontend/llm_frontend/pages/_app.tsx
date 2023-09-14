/*
import "@/styles/globals.css";
import { Inter } from "@next/font/google";
import type { AppProps } from "next/app";
import { RecoilRoot } from 'recoil';

const inter = Inter({ subsets: ["latin"] });

export default function App({ Component, pageProps }: AppProps<{}>) {
  return (
    <RecoilRoot>
      <main className={inter.className}>
        <Component {...pageProps} />
      </main>
    </RecoilRoot>
  );
}
*/

import "@/styles/globals.css"
import { Inter } from "@next/font/google"
import type { AppProps } from "next/app"
import { RecoilRoot } from 'recoil'
import { AuthProvider } from '../hooks/useAuth'

const inter = Inter({ subsets: ["latin"] });

export default function App({ Component, pageProps }: AppProps<{}>) {
    return (
        <AuthProvider>
            <RecoilRoot>
                <Component {...pageProps} />
            </RecoilRoot>
        </AuthProvider>
    );
}