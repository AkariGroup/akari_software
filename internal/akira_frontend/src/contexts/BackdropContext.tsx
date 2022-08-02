import React, {
  Dispatch,
  createContext,
  SetStateAction,
  useContext,
  useState,
} from "react";

const backdropContext = createContext<boolean>(false);
const setBackdropContext = createContext<Dispatch<SetStateAction<boolean>>>(
  () => undefined
);

export function useBackdropValue() {
  return useContext(backdropContext);
}
export function useSetBackdropValue() {
  return useContext(setBackdropContext);
}

export function BackdropProvider({ children }: { children: React.ReactNode }) {
  const [backdrop, setBackdrop] = useState<boolean>(false);

  return (
    <backdropContext.Provider value={backdrop}>
      <setBackdropContext.Provider value={setBackdrop}>
        {children}
      </setBackdropContext.Provider>
    </backdropContext.Provider>
  );
}
