import React, {
  Dispatch,
  createContext,
  SetStateAction,
  useContext,
} from "react";

export const darkmodeKey = "darkmode"
const darkmodeContext = createContext<boolean>(false);
const setDarkmodeContext = createContext<Dispatch<SetStateAction<boolean>>>(
  () => undefined
);

export function useDarkmodeValue() {
  return useContext(darkmodeContext);
}
export function useSetDarkmodeValue() {
  console.log(darkmodeContext);
  localStorage.setItem(darkmodeKey, useContext(darkmodeContext) ? "on" : "off");
  return useContext(setDarkmodeContext);
}

export function DarkModeProvider({ children }: { children: React.ReactNode }) {
  const [darkmode, setDarkmode] = React.useState(() => localStorage.getItem(darkmodeKey) === "on");
  return (
    <darkmodeContext.Provider value={darkmode}>
      <setDarkmodeContext.Provider value={setDarkmode}>
        {children}
      </setDarkmodeContext.Provider>
    </darkmodeContext.Provider>
  );
}
