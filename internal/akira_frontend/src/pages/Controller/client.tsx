import aspida from "@aspida/axios";
import { useMemo } from "react";
import axios, { AxiosRequestConfig } from "axios";
import { AspidaClient } from "aspida";
import api from "../../service-apis/akira-controller-server/$api";

export function getAspidaClient(): AspidaClient<AxiosRequestConfig> {
  const hostname = window.location.hostname;
  return aspida(axios, { baseURL: `//${hostname}:52001` });
}

export type AkiraControllerClient = ReturnType<
  typeof api<AspidaClient<AxiosRequestConfig<any>>>
>;

export function useAkiraControllerClient(): AkiraControllerClient {
  const client = useMemo(() => {
    return api(getAspidaClient());
  }, []);
  return client;
}
