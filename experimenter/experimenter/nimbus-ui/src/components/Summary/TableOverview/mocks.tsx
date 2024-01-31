/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
import React, { useState } from "react";
import TableQA from "src/components/Summary/TableQA";
import { ExperimentContextType } from "src/lib/contexts";
import { MOCK_CONFIG, MockedCache } from "src/lib/mocks";
import { MockExperimentContextProvider, RouterSlugProvider } from "src/lib/test-utils";
import { getConfig_nimbusConfig } from "src/types/getConfig";
import { getExperiment_experimentBySlug } from "src/types/getExperiment";
import { ExperimentInput, NimbusExperimentQAStatusEnum } from "src/types/globalTypes";
import TableOverview, { SubscriberParams } from "src/components/Summary/TableOverview";
import { UPDATE_EXPERIMENT_MUTATION } from "src/gql/experiments";
import { updateExperiment_updateExperiment } from "src/types/updateExperiment";

export const Subject = ({
  experiment,
  config = MOCK_CONFIG,
  context = {},
  mocks = [],
}: {
  experiment: getExperiment_experimentBySlug;
  config?: getConfig_nimbusConfig;
  context?: Partial<ExperimentContextType>;
  mocks?: React.ComponentProps<typeof MockedCache>["mocks"];
}) => {
  return (
    <RouterSlugProvider>
      <MockedCache {...{ config, mocks }}>
        <MockExperimentContextProvider
          value={{
            experiment: experiment,
            ...context,
          }}
        >
          <TableOverview {...{ experiment }} />
        </MockExperimentContextProvider>
      </MockedCache>
    </RouterSlugProvider>
  );
};

export const mockUpdateExperimentSubscribersMutation = (
  input: Partial<ExperimentInput>,
  {
    message = "success",
  }: {
    message?: string | Record<string, any>;
  },
) => {
  const updateExperiment: updateExperiment_updateExperiment = {
    message,
  };
  return {
    request: {
      query: UPDATE_EXPERIMENT_MUTATION,
      variables: {
        input,
      },
    },
    result: {
      errors: undefined as undefined | any[],
      data: {
        updateExperiment,
      },
    },
  };
};
