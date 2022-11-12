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
import { ApiClient } from "../../hooks/api";
import { ValidationMessages } from "../../libs/messages";
import CloseIcon from "@mui/icons-material/Close";

interface EditServiceRequest {
  display_name: string;
  description: string;
}
type Props = {
  service: Akira_protoService;
  client: ApiClient;
  onClose: () => void;
};

export function ServiceEditDrawer({ service, client, onClose }: Props) {
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<EditServiceRequest>();
  const setBusy = useSetBackdropValue();
  const onServiceEdit: SubmitHandler<EditServiceRequest> = useCallback(
    async (data) => {
      if (!client || !service.id) return;
      setBusy(true);
      try {
        await client.services._id(service.id).edit.post({
          body: {
            displayName: data.display_name,
            description: data.description,
          },
        });
        onClose();
      } finally {
        setBusy(false);
      }
    },
    [service, client, onClose, setBusy]
  );

  return (
    <Drawer
      anchor="right"
      open={true}
      onClose={onClose}
      PaperProps={{ sx: { width: { sm: "100%", md: "40vw" } } }}
    >
      <Stack margin={2} spacing={2}>
        <Box>
          <Stack direction="row" alignItems="center">
            <IconButton onClick={onClose}>
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
          defaultValue={service.displayName}
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
          defaultValue={service.description}
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
          onClick={onClose}
        >
          キャンセル
        </Button>
      </Stack>
    </Drawer>
  );
}
