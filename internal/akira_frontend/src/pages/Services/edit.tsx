import useAspidaSWR from "@aspida/swr";
import {
  Box,
  Button,
  Divider,
  Drawer,
  IconButton,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { useCallback } from "react";
import { Controller, SubmitHandler, useForm } from "react-hook-form";
import { Akira_protoService } from "../../api/@types";
import { useSetBackdropValue } from "../../contexts/BackdropContext";
import { ApiClient, useApiClient } from "../../hooks/api";
import { ValidationMessages } from "../../libs/messages";
import CloseIcon from "@mui/icons-material/Close";

export interface EditServiceRequest {
  id: string;
  display_name: string;
  description: string;
}
type Props = {
  service: Akira_protoService;
  client: ApiClient;
  onClose: () => void;
  onSubmit: SubmitHandler<EditServiceRequest>;
};

export function ServiceEditDrawer(props: Props) {
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<EditServiceRequest>();
  const setBusy = useSetBackdropValue();
  const client = useApiClient();
  const { mutate } = useAspidaSWR(client?.services, {
    enabled: !!client,
    refreshInterval: 5 * 1000, // in ms
  });
  const onServiceEdit: SubmitHandler<EditServiceRequest> = useCallback(
    async (data) => {
      if (!client) return;
      console.log(data);
      // TODO: Handle error (e.g. Directory name conflicts)
      const request: EditServiceRequest = {
        id: props.service.id ?? "",
        display_name: data.display_name,
        description: data.description,
      };
      setBusy(true);
      try {
        await client.services._id(request.id).edit.post({
          body: {
            displayName: request.display_name,
            description: request.description,
          },
        });
        props.onClose();
        mutate();
      } finally {
        setBusy(false);
      }
    },
    [client, props, setBusy, mutate]
  );

  return (
    <Drawer
      anchor="right"
      open={true}
      onClose={props.onClose}
      PaperProps={{ sx: { width: { sm: "100%", md: "40vw" } } }}
    >
      <Stack margin={2} spacing={2}>
        <Box>
          <Stack direction="row" alignItems="center">
            <IconButton onClick={props.onClose}>
              <CloseIcon />
            </IconButton>
            <Typography variant="h5" ml={1}>
              インスタンスの編集
            </Typography>
          </Stack>
          <Divider sx={{ mt: 1 }} />
        </Box>
        <Controller
          name="display_name"
          control={control}
          defaultValue={props.service.displayName}
          rules={{
            required: ValidationMessages.Required,
          }}
          render={({ field }) => (
            <TextField
              {...field}
              label="表示名"
              variant="filled"
              error={!!errors.display_name}
              helperText={errors.display_name && errors.display_name.message}
            />
          )}
        />
        <Controller
          name="description"
          control={control}
          defaultValue={props.service.description}
          render={({ field }) => (
            <TextField
              {...field}
              multiline
              rows={5}
              label="概要"
              variant="filled"
              fullWidth
              error={!!errors.description}
              helperText={errors.description && errors.description.message}
            />
          )}
        />
        <Button
          type="button"
          variant="contained"
          onClick={handleSubmit(onServiceEdit)}
        >
          変更
        </Button>
        <Button
          type="button"
          color="error"
          variant="outlined"
          onClick={props.onClose}
        >
          キャンセル
        </Button>
      </Stack>
    </Drawer>
  );
}
