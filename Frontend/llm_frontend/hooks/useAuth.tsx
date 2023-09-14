import {
    createUserWithEmailAndPassword,
    onAuthStateChanged,
    signInWithEmailAndPassword,
    signOut,
    User,
} from 'firebase/auth'
import { useRouter } from 'next/router'
import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { auth } from '../firebase'

interface IAuth {
    user: User | null
    signUp: (email: string, password: string) => Promise<void>
    signIn: (email: string, password: string) => Promise<void>
    logout: () => Promise<void>
    error: string | null
    loading: boolean
}

const AuthContext = createContext<IAuth>({
    user: null,
    signUp: async () => {},
    signIn: async () => {},
    logout: async () => {},
    error: null,
    loading: false,
})

interface AuthProviderProps {
    children: React.ReactNode
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
    const router = useRouter()
    const [user, setUser] = useState<User | null>(null)
    const [error, setError] = useState(null)
    const [initialLoading, setInitialLoading] = useState(true)
    const [loading, setLoading] = useState(false)

    useEffect(
        () =>
            onAuthStateChanged(auth, (user) => {
                if (user) {
                    // Logged in...
                    setUser(user)
                    setLoading(false)
                } else {
                    // Not logged in...
                    setUser(null)
                    setLoading(true)
                    router.push('/Login')
                }

                setInitialLoading(false)
            }),
        [auth]
    )

    const signUp = async (email: string, password: string) => {
        setLoading(true)

        await createUserWithEmailAndPassword(auth, email, password)
            .then((userCredential) => {
                setUser(userCredential.user)
                router.push('/')
                setLoading(false)
            })
            .catch((error) => alert(error.message))
            .finally(() => setLoading(false))
    }
    /*
    const signIn = async (email: string, password: string) => {
        setLoading(true)
        await signInWithEmailAndPassword(auth, email, password)
            .then((userCredential) => {
                setUser(userCredential.user)
                router.push('/')
                setLoading(false)
            })
            .catch((error) => alert(error.message))
            .finally(() => setLoading(false))
    }
    */
    // Inside your useAuth hook...
const signIn = async (email: string, password: string, otp?: string) => {
    setLoading(true)
    await signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            if (otp) {
                return fetch('http://localhost:8080/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Basic ' + btoa(email + ':' + password)
                    },
                    body: JSON.stringify({ OTP: otp })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        setUser(userCredential.user)
                        router.push('/')
                    } else {
                        throw new Error('OTP_REQUIRED')
                    }
                })
            } else {
                setUser(userCredential.user)
                router.push('/')
            }
        })
        .catch((error) => {
            if (error.message === 'OTP_REQUIRED') {
                throw error;
            }
            alert(error.message);
        })
        .finally(() => setLoading(false))
}

    const logout = async () => {
        setLoading(true)

        signOut(auth)
            .then(() => {
                setUser(null)
            })
            .catch((error) => alert(error.message))
            .finally(() => setLoading(false))
    }

    const memoedValue = useMemo(
        () => ({ user, signUp, signIn, error, loading, logout }),
        [user, loading, error]
    )

    return (
        <AuthContext.Provider value={memoedValue}>
            {!initialLoading && children}
        </AuthContext.Provider>
    )
}

// Let's only export the `useAuth` hook instead of the context.
// We only want to use the hook directly and never the context comopnent.
export default function useAuth() {
    return useContext(AuthContext)
}