//atom is a good library in react for defining
//a sort of state machine for react components
//and state of the webpage. Every stage is

// https://recoiljs.org/docs/introduction/core-concepts
import { atom } from 'recoil'

//every state is an atom
export const OTPmodalState = atom(
    {
        key: 'OPTmodalState',
        default: false,
    }
)

export const modalState = atom(
    {
        key: 'modalState',
        default: false,
    }
)
//every state in Recoil has a different key and value

export const recommendationState = atom(
    {
        key: 'recommendationState',
        default: false,
    }
)

export const TwitterSearchState = atom(
    {
        key: "TwitterSearchState",
        default: false,
    }
)