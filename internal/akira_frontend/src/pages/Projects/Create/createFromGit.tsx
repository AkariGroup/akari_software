import { Controller, SubmitHandler, useForm } from "react-hook-form";
import { useApiClient } from "../../../hooks/api";
import { Akira_protoCreateProjectFromGitRequest } from "../../../api/@types";
import { useCallback, useState } from "react";
import {
  Button,
  FormControlLabel,
  FormGroup,
  Grid,
  Stack,
  Switch,
  TextField,
} from "@mui/material";
import useAspidaSWR from "@aspida/swr";
import { useNavigate } from "react-router-dom";
import { ValidationMessages } from "../../../libs/messages";
import {
  ValidBranchNamePattern,
  ValidGitUrlPattern,
  ValidNamePattern,
} from "../validNamePattern";
import { CancelButton } from "../../../components/CancelButton";
type CreateProjectFromGitInputs = {
  branch?: string;
  dirname?: string;
  gitUrl: string;
};

export function CreateProjectFromGit() {
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
  } = useForm<CreateProjectFromGitInputs>();
  const navigate = useNavigate();

  const client = useApiClient();
  const { data: templates } = useAspidaSWR(client.templates, {
    enabled: !!client,
  });
  const onSubmit: SubmitHandler<CreateProjectFromGitInputs> = useCallback(
    async (data) => {
      if (!client) return;

      const request: Akira_protoCreateProjectFromGitRequest = {
        branch: data.branch !== "" ? data.branch : undefined,
        dirname: customPath ? data.dirname : undefined,
        gitUrl: data.gitUrl,
      };
      // TODO: Handle error (e.g. Directory name conflicts)
      const res = await client.projects.create.git.post({
        body: request,
      });
      const projectId = res.body.id;

      navigate(`/projects/details?id=${projectId}`);
    },
    [customPath, client, navigate]
  );

  const customPathElement = customPath ? (
    <Controller
      name="dirname"
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
          error={!!errors.dirname}
          helperText={errors.dirname && errors.dirname.message}
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
      <Grid item sm={12}>
        <Stack spacing={2}>
          <Controller
            name="gitUrl"
            control={control}
            rules={{
              required: ValidationMessages.Required,
              pattern: {
                value: ValidGitUrlPattern,
                message: ValidationMessages.InvalidCharacter,
              },
            }}
            defaultValue=""
            render={({ field }) => (
              <TextField
                {...field}
                required
                label="git URL"
                variant="filled"
                error={!!errors.gitUrl}
                helperText={errors.gitUrl && errors.gitUrl.message}
              />
            )}
          />
          <Controller
            name="branch"
            control={control}
            rules={{
              pattern: {
                value: ValidBranchNamePattern,
                message: ValidationMessages.InvalidCharacter,
              },
            }}
            defaultValue=""
            render={({ field }) => (
              <TextField
                {...field}
                label="gitブランチ名"
                variant="filled"
                error={!!errors.branch}
                helperText={errors.branch && errors.branch.message}
              />
            )}
          />
          <FormGroup>
            <FormControlLabel
              control={
                <Switch
                  color="secondary"
                  checked={customPath}
                  onChange={handleCustomPathChange}
                />
              }
              label="&nbsp;プロジェクト名と異なるディレクトリ名を指定する"
            />
          </FormGroup>

          {customPathElement}
        </Stack>
      </Grid>
      <Grid item>
        <Button
          type="button"
          variant="contained"
          onClick={handleSubmit(onSubmit)}
        >
          作成
        </Button>
      </Grid>
      <Grid item>
        <CancelButton />
      </Grid>
    </Grid>
  );
}
