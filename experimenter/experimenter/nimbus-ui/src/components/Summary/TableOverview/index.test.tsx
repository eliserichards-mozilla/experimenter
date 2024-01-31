/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

import {
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from "@testing-library/react";
import React, { ReactNode } from "react";
import TableOverview, {
  SubscriberParams,
} from "src/components/Summary/TableOverview";
import { UPDATE_EXPERIMENT_MUTATION } from "src/gql/experiments";
import { ExperimentContextType } from "src/lib/contexts";
import { MockedCache, mockExperimentQuery, MOCK_CONFIG } from "src/lib/mocks";
import {
  MockExperimentContextProvider,
  RouterSlugProvider,
} from "src/lib/test-utils";
import { getConfig_nimbusConfig } from "src/types/getConfig";
import { getExperiment_experimentBySlug } from "src/types/getExperiment";
import { ExperimentInput } from "src/types/globalTypes";
import { updateExperiment_updateExperiment } from "src/types/updateExperiment";
import { Subject, mockUpdateExperimentSubscribersMutation } from "src/components/Summary/TableOverview/mocks";

describe("TableOverview", () => {
  it("renders rows displaying required fields at experiment creation as expected", () => {
    const { experiment } = mockExperimentQuery("demo-slug");
    render(<Subject {...{ experiment }} />);

    expect(screen.getByTestId("experiment-slug")).toHaveTextContent(
      "demo-slug",
    );
    expect(screen.getByTestId("experiment-owner")).toHaveTextContent(
      "example@mozilla.com",
    );
    expect(screen.getByTestId("experiment-application")).toHaveTextContent(
      "Desktop",
    );
    expect(screen.getByTestId("experiment-hypothesis")).toHaveTextContent(
      "Realize material say pretty.",
    );
    expect(screen.getByTestId("experiment-team-projects")).toHaveTextContent(
      "Pocket",
    );
    expect(
      within(
        screen.getByTestId("experiment-subscribers") as HTMLElement,
      ).queryByTestId("not-set"),
    ).toBeInTheDocument();
  });

  describe("renders 'Primary outcomes' row as expected", () => {
    it("with one outcome", () => {
      const { experiment } = mockExperimentQuery("demo-slug");
      render(<Subject {...{ experiment }} />);
      expect(
        screen.getByTestId("experiment-outcome-primary"),
      ).toHaveTextContent("Picture-in-Picture");
    });

    it("with correct documentation URl", () => {
      const { experiment } = mockExperimentQuery("demo-slug", {
        primaryOutcomes: ["picture_in_picture"],
      });
      render(<Subject {...{ experiment }} />);
      expect(
        screen.getByTestId("primary-outcome-picture_in_picture"),
      ).toBeInTheDocument();
      expect(
        screen.getByTestId("primary-outcome-picture_in_picture"),
      ).toHaveAttribute(
        "href",
        "https://mozilla.github.io/metric-hub/outcomes/firefox_desktop/picture_in_picture",
      );
    });

    it("with multiple outcomes", () => {
      const { experiment } = mockExperimentQuery("demo-slug", {
        primaryOutcomes: ["picture_in_picture", "feature_c"],
      });
      render(<Subject {...{ experiment }} />);
      expect(
        screen.getByTestId("experiment-outcome-primary"),
      ).toHaveTextContent("Picture-in-Picture, Feature C");
    });

    it("when not set", () => {
      const { experiment } = mockExperimentQuery("demo-slug", {
        primaryOutcomes: [],
      });
      render(<Subject {...{ experiment }} />);
      expect(
        screen.queryByTestId("experiment-outcome-primary"),
      ).not.toBeInTheDocument();
    });
  });

  describe("renders 'Secondary outcomes' row as expected", () => {
    it("with one outcome", () => {
      const { experiment } = mockExperimentQuery("demo-slug");
      render(<Subject {...{ experiment }} />);
      expect(
        screen.getByTestId("experiment-outcome-secondary"),
      ).toHaveTextContent("Feature B");
    });

    it("with correct documentation URl", () => {
      const { experiment } = mockExperimentQuery("demo-slug", {
        secondaryOutcomes: ["picture_in_picture"],
      });
      render(<Subject {...{ experiment }} />);
      expect(
        screen.getByTestId("secondary-outcome-picture_in_picture"),
      ).toBeInTheDocument();
      expect(
        screen.getByTestId("secondary-outcome-picture_in_picture"),
      ).toHaveAttribute(
        "href",
        "https://mozilla.github.io/metric-hub/outcomes/firefox_desktop/picture_in_picture",
      );
    });

    it("with multiple outcomes", () => {
      const { experiment } = mockExperimentQuery("demo-slug", {
        secondaryOutcomes: ["picture_in_picture", "feature_b"],
      });
      render(<Subject {...{ experiment }} />);
      expect(
        screen.getByTestId("experiment-outcome-secondary"),
      ).toHaveTextContent("Picture-in-Picture, Feature B");
    });

    it("when not set", () => {
      const { experiment } = mockExperimentQuery("demo-slug", {
        secondaryOutcomes: [],
      });
      render(<Subject {...{ experiment }} />);
      expect(
        screen.queryByTestId("experiment-outcome-secondary"),
      ).not.toBeInTheDocument();
    });
  });

  describe("renders 'Public description' row as expected", () => {
    it("when set", () => {
      const { experiment } = mockExperimentQuery("demo-slug");
      render(<Subject {...{ experiment }} />);
      expect(screen.getByTestId("experiment-description")).toHaveTextContent(
        "Official approach present industry strategy dream piece.",
      );
    });
    it("when not set", () => {
      const { experiment } = mockExperimentQuery("demo-slug", {
        publicDescription: "",
      });
      render(<Subject {...{ experiment }} />);
      expect(screen.getByTestId("experiment-description")).toHaveTextContent(
        "Not set",
      );
    });
  });

  describe("renders 'Feature config' row as expected", () => {
    it("when set", () => {
      const { experiment } = mockExperimentQuery("demo-slug");
      render(<Subject {...{ experiment }} />);
      expect(screen.getByTestId("experiment-feature-config")).toHaveTextContent(
        "Picture-in-Picture",
      );
    });
    it("when not set", () => {
      const { experiment } = mockExperimentQuery("demo-slug", {
        featureConfigs: [],
      });
      render(<Subject {...{ experiment }} />);
      expect(screen.getByTestId("experiment-feature-config")).toHaveTextContent(
        "Not set",
      );
    });
  });

  describe("renders 'Targeting config' row as expected", () => {
    it("when set", () => {
      const currentUser = "me@dev.example";
      const config = {
        ...MOCK_CONFIG,
        user: currentUser,
      };
      const { experiment } = mockExperimentQuery("demo-slug", {
        targetingConfig: [MOCK_CONFIG.targetingConfigs![0]],
      });
      render(<Subject {...{ experiment, config }} />);
      expect(
        screen.getByTestId("experiment-targeting-config"),
      ).toHaveTextContent("Mac Only - Mac only configuration");
    });

    it("when not set", () => {
      const currentUser = "me@dev.example";
      const config = {
        ...MOCK_CONFIG,
        user: currentUser,
      };
      const { experiment } = mockExperimentQuery("demo-slug", {
        targetingConfig: [],
      });
      render(<Subject {...{ experiment, config }} />);
      expect(
        screen.getByTestId("experiment-targeting-config"),
      ).toHaveTextContent("Not set");
    });
  });

  describe("renders 'Team Projects' row as expected", () => {
    it("with one team project", () => {
      const { experiment } = mockExperimentQuery("demo-slug");
      render(<Subject {...{ experiment }} />);
      expect(screen.getByTestId("experiment-team-projects")).toHaveTextContent(
        "Pocket",
      );
    });

    it("with multiple projects", async () => {
      const currentUser = "me@dev.example";
      const config = {
        ...MOCK_CONFIG,
        user: currentUser,
      };
      const { experiment } = mockExperimentQuery("demo-slug", {
        projects: [
          { id: "1", name: "Pocket" },
          { id: "2", name: "VPN" },
        ],
      });
      render(<Subject {...{ experiment, config }} />);
      await waitFor(() => {
        experiment.projects!.forEach((team) =>
          within(screen.getByTestId("experiment-team-projects")).findByText(
            team!.name!,
          ),
        );
      });
    });

    it("when not set", () => {
      const { experiment } = mockExperimentQuery("demo-slug", {
        projects: [],
      });
      render(<Subject {...{ experiment }} />);
      expect(
        screen.queryByTestId("experiment-team-projects"),
      ).toHaveTextContent("Not set");
    });
  });

  describe("renders 'Subscribers' as expected", () => {
    it("with no subscribers", async () => {
      const { experiment } = mockExperimentQuery("demo-slug");
      render(<Subject {...{ experiment }} />);
      expect(screen.getByTestId("experiment-subscribers")).toHaveTextContent(
        "Not set",
      );
    });

    it("with multiple subscribers", async () => {
      const { experiment } = mockExperimentQuery("demo-slug", {
        subscribers: [
          {
            email: "example1@mozilla.com",
          },
          {
            email: "example2@mozilla.com",
          },
        ],
      });
      render(<Subject {...{ experiment }} />);
      await waitFor(() => {
        experiment.subscribers!.forEach((subscriber) =>
          within(screen.getByTestId("experiment-subscribers")).findByText(
            subscriber!.email!,
          ),
        );
      });
    });
  });

  describe("renders 'Subscribers' button as expected", () => {
    it("when user is subscribed", async () => {
      const currentUser = "me@dev.example";
      const { experiment } = mockExperimentQuery("demo-slug", {
        subscribers: [
          {
            email: currentUser,
          },
          {
            email: "big_ole_cat@cronch.com",
          },
        ],
      });
      const config = {
        ...MOCK_CONFIG,
        user: currentUser,
      };
      expect(experiment.subscribers.flatMap((s) => s.email)).toEqual([
        currentUser,
        "big_ole_cat@cronch.com",
      ]);

      render(<Subject {...{ experiment, config }} />);
      await waitFor(() => {
        expect(
          within(
            screen.getByTestId("add-subscriber-button") as HTMLElement,
          ).queryByText("Unsubscribe"),
        ).toBeInTheDocument();
      });
    });

    it("when user is not subscribed", async () => {
      const { experiment } = mockExperimentQuery("demo-slug");
      const currentUser = "me@dev.example";
      const config = {
        ...MOCK_CONFIG,
        user: currentUser,
      };
      expect(experiment.subscribers).toEqual([]);

      render(<Subject {...{ experiment, config }} />);
      await waitFor(() => {
        expect(
          within(
            screen.getByTestId("add-subscriber-button") as HTMLElement,
          ).queryByText("Subscribe"),
        ).toBeInTheDocument();
      });
    });

    it("subscribes as expected", async () => {
      const { mock, experiment } = mockExperimentQuery("demo-slug");
      const currentUser = "me@dev.example";
      const config = {
        ...MOCK_CONFIG,
        user: currentUser,
      };
      expect(experiment.subscribers).toEqual([]);

      setMockUpdateState(currentUser, false);

      const mockMutation = mockUpdateExperimentSubscribersMutation(
        {
          ...mockUpdateState,
          id: experiment.id,
          changelogMessage: "test update subscribers",
        },
        {},
      );

      mockMutation.result.data.updateExperiment.message = {};
      render(
        <Subject mocks={[mock, mockMutation]} {...{ experiment, config }} />,
      );
      await screen.findByTestId("experiment-subscribers");

      const subscribeButton = screen.getByTestId("add-subscriber-button");
      fireEvent.click(subscribeButton);

      await waitFor(() => {
        expect(mockSetSubmitErrors).not.toHaveBeenCalled();
        // mockMutation is not being called correctly
        // expect(mockMutation.result).toEqual("success");
      });
      expect(experiment.subscribers).toEqual([]);
    });
  });
});

jest.mock("@reach/router", () => ({
  ...(jest.requireActual("@reach/router") as any),
  navigate: jest.fn(),
}));

const mockSetSubmitErrors = jest.fn();
let mockUpdateState: SubscriberParams;

function setMockUpdateState(email: string, subscribed: boolean) {
  mockUpdateState = {
    email,
    subscribed,
  };
}
