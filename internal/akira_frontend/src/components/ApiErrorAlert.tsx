import { Alert, AlertTitle } from "@mui/material";
import { ApiError } from "../libs/types";

type Props = {
  error?: ApiError;
};

export function ApiErrorAlert(props: Props) {
  return (
    <Alert severity="error">
      <AlertTitle>Error</AlertTitle>
      {props.error?.message}
    </Alert>
  );
}
