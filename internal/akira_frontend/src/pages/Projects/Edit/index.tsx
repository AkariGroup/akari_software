import {
  Controller,
  SubmitHandler,
  useForm,
} from "react-hook-form";
import { useApiClient } from "../../../hooks/api";
import {
  Akira_protoEditProjectRequest,
  Akira_protoProjectManifest,
} from "../../../api/@types";
import { useCallback } from "react";
import {
  Button,
  Grid,
  Stack,
  TextField,
} from "@mui/material";
import useAspidaSWR from "@aspida/swr";
import { useNavigate, useSearchParams} from "react-router-dom";
import { ValidationMessages } from "../../../libs/messages";
import { ValidNamePattern } from "../validNamePattern";

type EditProjectFromTemplateInputs = {
  id: string;
  manifest: Akira_protoProjectManifest;
};

export function ProjectsEdit() {
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<EditProjectFromTemplateInputs>();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const projectId = searchParams.get("id") as string;
  const client = useApiClient();
  const { data: project } = useAspidaSWR(client?.projects.detail, {
    query: {
      id: projectId,
    },
    enabled: !!projectId && !!client,
  });
  const prevPage = () => {
    navigate(-1);
  }

  const onSubmit: SubmitHandler<EditProjectFromTemplateInputs> = useCallback(
    async (data) => {
      if (!client) return;

      const request: Akira_protoEditProjectRequest = {
        manifest: data.manifest,
        id: projectId,
      };
      console.log(data.manifest.name);
      // TODO: Handle error (e.g. Directory name conflicts)
      const res = await client.projects.edit.post({
        body: request,
      });

      navigate(`/projects/details?id=${projectId}`);
    },
    [client, navigate]
  );

  if (!project) {
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
            defaultValue={project.manifest?.name}
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
            defaultValue={project.manifest?.author}
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
            defaultValue={project.manifest?.url}
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
          defaultValue={project.manifest?.description}
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
          variant="outlined"
          color="error"
          onClick={prevPage}
        >
          キャンセル
        </Button>
      </Grid>
    </Grid>
  );
}
