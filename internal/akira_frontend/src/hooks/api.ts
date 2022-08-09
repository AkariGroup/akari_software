import aspida from "@aspida/axios";
import { useMemo } from "react";
import api from "../api/$api";
import axios, { AxiosRequestConfig } from "axios";
import { AspidaClient } from "aspida";

export function getAspidaClient(): AspidaClient<AxiosRequestConfig> {
  return aspida(axios, { baseURL: "/api" });
}

export type ApiClient = ReturnType<typeof api<AspidaClient<AxiosRequestConfig<any>>>>;

export function useApiClient(): ApiClient {
  const client = useMemo(() => {
    return api(getAspidaClient());
  }, []);
  return client;
}
