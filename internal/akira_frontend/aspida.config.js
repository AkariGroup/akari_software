module.exports = [
  {
    input: "src/api",
    outputEachDir: true,
    openapi: { inputFile: "openapiv2/akira/apidocs.swagger.yaml" }
  },
  {
    input: "src/service-apis/akira-controller-server",
    outputEachDir: true,
    openapi: { inputFile: "openapiv2/akira_controller_server/openapi.json" }
  },
]
