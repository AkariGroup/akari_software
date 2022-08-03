import useAspidaSWR from "@aspida/swr";
import {
  Box,
  Button,
  Divider,
  Drawer,
  FormControl,
  FormHelperText,
  IconButton,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import {
  Controller,
  ControllerRenderProps,
  FieldError,
  SubmitHandler,
  useForm,
} from "react-hook-form";
import {
  Akira_protoCreateInstanceRequest,
  Akira_protoServiceImage,
} from "../../api/@types";
import { ApiClient } from "../../hooks/api";
import { ValidationMessages } from "../../libs/messages";

type ServiceImageSelectorProps = {
  fields: ControllerRenderProps<Akira_protoCreateInstanceRequest, "imageId">;
  images?: Akira_protoServiceImage[];
  error?: FieldError;
};

function ServiceImageItem({ image }: { image: Akira_protoServiceImage }) {
  return (
    <Stack>
      <Typography whiteSpace="nowrap">
        <Box component="span" fontWeight="bold">
          {image.displayName}
        </Box>
        &nbsp; - Version: {image.version}, Name: {image.name}&nbsp;
        <Box component="span" color="text.secondary">
          (ID: {image.id})
        </Box>
      </Typography>
      <Typography
        display="inline-block"
        maxWidth="40vw"
        overflow="hidden"
        textOverflow="ellipsis"
        color="text.secondary"
      >
        {image.description}
      </Typography>
    </Stack>
  );
}

function ServiceImageSelector(props: ServiceImageSelectorProps) {
  const error = !!props.error;
  return (
    <FormControl fullWidth variant="filled" error={error}>
      <InputLabel id="image-selector-label">サービスイメージ</InputLabel>
      <Select
        {...props.fields}
        labelId="image-selector-label"
        label="サービスイメージ"
        defaultValue=""
        renderValue={(e) => {
          const item = props.images?.find((s) => s.id === e);
          return `${item?.displayName} @ ${item?.version}`;
        }}
        error={error}
        onChange={(val) => props.fields.onChange(val)}
      >
        {props.images?.map((t) => (
          <MenuItem key={t.id} value={t.id}>
            <ServiceImageItem image={t} />
          </MenuItem>
        ))}
      </Select>
      {error ? <FormHelperText>{props.error?.message}</FormHelperText> : <></>}
    </FormControl>
  );
}

type Props = {
  client: ApiClient;
  onClose: () => void;
  onSubmit: SubmitHandler<Akira_protoCreateInstanceRequest>;
};

export function InstanceCreateDrawer(props: Props) {
  const { data: images } = useAspidaSWR(props.client?.images, {
    enabled: !!props.client,
  });
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<Akira_protoCreateInstanceRequest>();

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
              インスタンスの作成
            </Typography>
          </Stack>
          <Divider sx={{ mt: 1 }} />
        </Box>
        <Controller
          name="displayName"
          control={control}
          defaultValue=""
          rules={{
            required: ValidationMessages.Required,
          }}
          render={({ field }) => (
            <TextField
              {...field}
              label="表示名"
              variant="filled"
              error={!!errors.displayName}
              helperText={errors.displayName && errors.displayName.message}
            />
          )}
        />

        <Controller
          name="description"
          control={control}
          defaultValue=""
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

        <Controller
          name="imageId"
          control={control}
          defaultValue=""
          rules={{
            required: ValidationMessages.Required,
          }}
          render={({ field }) => (
            <ServiceImageSelector
              fields={field}
              images={images?.images}
              error={errors.imageId}
            />
          )}
        />
        <Button
          type="button"
          variant="contained"
          onClick={handleSubmit(props.onSubmit)}
        >
          作成
        </Button>
      </Stack>
    </Drawer>
  );
}
