import {
  Controller,
  ControllerRenderProps,
  FieldError,
  SubmitHandler,
  useForm,
} from "react-hook-form";
import { useApiClient } from "../../../hooks/api";
import {
  //Akira_protoEditLocalProjectRequest,
  Akira_protoProjectManifest,
} from "../../../api/@types";
import { useCallback, useState } from "react";
import {
  Box,
  Button,
  FormControl,
  FormControlLabel,
  FormGroup,
  FormHelperText,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  Switch,
  TextField,
  Typography,
} from "@mui/material";
import useAspidaSWR from "@aspida/swr";
import { useNavigate, Link } from "react-router-dom";
import { ValidationMessages } from "../../../libs/messages";

const ValidNamePattern = /^[A-Za-z0-9-_]+$/;

type Akira_protoEditLocalProjectRequest = {
  dirname?: string | undefined
  manifest?: Akira_protoProjectManifest | undefined
  templateId?: string | undefined
}

type EditProjectFromTemplateInputs = {
  path: string;
  templateId: string;
  manifest: Akira_protoProjectManifest;
};

export function ProjectsEdit() {
  const [customPath, setCustomPath] = useState(false);
  const handleCustomPathChange = useCallback(
    (_: any, checked: boolean) => {
      setCustomPath(checked);
    },
    [setCustomPath]
  );
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<EditProjectFromTemplateInputs>();
  const navigate = useNavigate();

  const client = useApiClient();
  const { data: templates } = useAspidaSWR(client.templates, {
    enabled: !!client,
  });
  const onSubmit: SubmitHandler<EditProjectFromTemplateInputs> = useCallback(
    async (data) => {
      if (!client) return;

      const request: Akira_protoEditLocalProjectRequest = {
        dirname: customPath ? data.path : data.manifest.name,
        manifest: data.manifest,
        templateId: data.templateId,
      };
      // TODO: Handle error (e.g. Directory name conflicts)
      const res = await client.projects.create.local.post({
        body: request,
      });
      const projectId = res.body.id;

      navigate(`/projects/details?id=${projectId}`);
    },
    [customPath, client, navigate]
  );

  const customPathElement = customPath ? (
    <Controller
      name="path"
      control={control}
      rules={{
        required: ValidationMessages.Required,
        pattern: {
          value: ValidNamePattern,
          message: ValidationMessages.InvalidCharacter,
        },
      }}
      defaultValue=""
      render={({ field }) => (
        <TextField
          {...field}
          required
          label="ディレクトリ名"
          variant="filled"
          error={!!errors.path}
          helperText={errors.path && errors.path.message}
        />
      )}
    />
  ) : (
    <></>
  );

  if (!client || !templates) {
    return <></>;
  }
  return (
    <Grid
      container
      component="form"
      spacing={2}
      padding={2}
      noValidate
      onSubmit={handleSubmit(onSubmit)}
    >
      <Grid item sm={12} md={6}>
        <Stack spacing={2}>
          <Controller
            name="manifest.name"
            control={control}
            rules={{
              required: ValidationMessages.Required,
              pattern: {
                value: ValidNamePattern,
                message: ValidationMessages.InvalidCharacter,
              },
            }}
            defaultValue=""
            render={({ field }) => (
              <TextField
                {...field}
                required
                label="プロジェクト名"
                variant="filled"
                error={!!errors.manifest?.name}
                helperText={
                  errors.manifest?.name && errors.manifest?.name.message
                }
              />
            )}
          />

          <Controller
            name="manifest.author"
            control={control}
            defaultValue=""
            render={({ field }) => (
              <TextField
                {...field}
                label="作者名"
                variant="filled"
                error={!!errors.manifest?.author}
                helperText={
                  errors.manifest?.author && errors.manifest?.author.message
                }
              />
            )}
          />
          <Controller
            name="manifest.url"
            control={control}
            defaultValue=""
            render={({ field }) => (
              <TextField
                {...field}
                label="URL"
                variant="filled"
                error={!!errors.manifest?.url}
                helperText={
                  errors.manifest?.url && errors.manifest?.url.message
                }
              />
            )}
          />

        </Stack>
      </Grid>
      <Grid item sm={12} md={6}>
        <Controller
          name="manifest.description"
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
              error={!!errors.manifest?.description}
              helperText={
                errors.manifest?.description &&
                errors.manifest?.description.message
              }
            />
          )}
        />
      </Grid>
      <Grid item md={12}>
        <Button
          type="button"
          variant="contained"
          onClick={handleSubmit(onSubmit)}
        >
          変更
        </Button>
        &nbsp;
        &nbsp;
        <Button
          type="button"
          variant="contained"
          component={Link} to ="/projects"
        >
          キャンセル
        </Button>
      </Grid>
    </Grid>
  );
}
