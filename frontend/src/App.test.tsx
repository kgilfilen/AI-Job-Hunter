import { cleanup, render, screen, fireEvent } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import App from "./App";

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

type MockApiResponses = {
  attention?: unknown[];
  activity?: unknown[];
  applications?: unknown[];
  activityTypes?: string[];
};

function mockApi({
  attention = [],
  activity = [],
  applications = [],
  activityTypes = [],
}: MockApiResponses = {}) {
  vi.spyOn(globalThis, "fetch").mockImplementation((url) => {
    if (url === "http://127.0.0.1:8000/applications/needs-attention") {
      return Promise.resolve({
        ok: true,
        json: async () => attention,
      } as Response);
    }

    if (url === "http://127.0.0.1:8000/activity/today") {
      return Promise.resolve({
        ok: true,
        json: async () => activity,
      } as Response);
    }

    if (url === "http://127.0.0.1:8000/applications") {
      return Promise.resolve({
        ok: true,
        json: async () => applications,
      } as Response);
    }

    if (url === "http://127.0.0.1:8000/activity-types") {
      return Promise.resolve({
        ok: true,
        json: async () => activityTypes,
      } as Response);
    }

    return Promise.reject(new Error(`Unexpected fetch URL: ${url}`));
  });
}

describe("App", () => {
  it("shows application details when an application is selected", async () => {
    mockApi({
      applications: [
        {
          application_id: 7,
          job_id: 42,
          status: "APPLIED",
          job_title: "Senior SDET",
          company: "Applied Systems",
        },
      ],
    });

    render(<App />);

    const applicationButton = await screen.findByRole("button", {
      name: "Senior SDET",
    });

    applicationButton.click();

    expect(await screen.findByText("Application Details")).toBeInTheDocument();
  });
  it("shows an empty Applications message when none are tracked", async () => {
    mockApi({
      applications: [],
    });

    render(<App />);

    expect(
      await screen.findByText("No tracked applications yet."),
    ).toBeInTheDocument();
  });
  it("shows tracked applications returned by the API", async () => {
    mockApi({
      applications: [
        {
          application_id: 7,
          job_id: 42,
          status: "APPLIED",
          job_title: "Senior SDET",
          company: "Applied Systems",
        },
      ],
    });

    render(<App />);

    expect(await screen.findByText("Applications")).toBeInTheDocument();

    expect(screen.getByText("Senior SDET")).toBeInTheDocument();

    expect(screen.getByText("Applied Systems")).toBeInTheDocument();

    expect(screen.getByText("Status: APPLIED")).toBeInTheDocument();
  });
  it("shows the empty Needs Attention message", async () => {
    mockApi();

    render(<App />);

    expect(
      await screen.findByText("No application follow-ups are currently due."),
    ).toBeInTheDocument();
  });

  it("shows application details when attention is required", async () => {
    mockApi({
      attention: [
        {
          application_id: 7,
          job_id: 42,
          status: "APPLIED",
          next_action: "Follow up with recruiter",
          follow_up_at: "2026-08-12T15:00:00+00:00",
          job_title: "Senior SDET",
          company: "Applied Systems",
        },
      ],
    });

    render(<App />);

    expect(await screen.findByText("Senior SDET")).toBeInTheDocument();

    expect(screen.getByText("Applied Systems")).toBeInTheDocument();

    expect(screen.getByText("Status: APPLIED")).toBeInTheDocument();

    expect(
      screen.getByText("Next action: Follow up with recruiter"),
    ).toBeInTheDocument();
  });

  it("shows recent activity returned by the API", async () => {
    mockApi({
      activity: [
        {
          event_id: 12,
          application_id: 7,
          event_type: "INTERVIEW_COMPLETED",
          occurred_at: "2026-08-12T18:30:00+00:00",
          notes: "Second interview completed.",
          job_id: 42,
          job_title: "Senior SDET",
          company: "Applied Systems",
        },
      ],
    });

    render(<App />);

    expect(await screen.findByText("INTERVIEW_COMPLETED")).toBeInTheDocument();

    expect(screen.getByText("Senior SDET")).toBeInTheDocument();

    expect(screen.getByText("Applied Systems")).toBeInTheDocument();

    expect(screen.getByText("Second interview completed.")).toBeInTheDocument();
  });

  it("submits a new activity with the selected values", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockImplementation((url, options) => {
        if (
          url === "http://127.0.0.1:8000/applications/needs-attention" ||
          url === "http://127.0.0.1:8000/activity/today"
        ) {
          return Promise.resolve({
            ok: true,
            json: async () => [],
          } as Response);
        }

        if (url === "http://127.0.0.1:8000/applications") {
          return Promise.resolve({
            ok: true,
            json: async () => [
              {
                application_id: 7,
                job_id: 42,
                status: "APPLIED",
                job_title: "Senior SDET",
                company: "Applied Systems",
              },
            ],
          } as Response);
        }

        if (url === "http://127.0.0.1:8000/activity-types") {
          return Promise.resolve({
            ok: true,
            json: async () => ["Interview completed", "Follow-up sent"],
          } as Response);
        }

        if (
          url === "http://127.0.0.1:8000/activity" &&
          options?.method === "POST"
        ) {
          return Promise.resolve({
            ok: true,
            json: async () => ({
              event_id: 99,
              application_id: 7,
              event_type: "Interview completed",
              occurred_at: "2026-08-12T20:00:00+00:00",
              notes: "Second interview completed.",
            }),
          } as Response);
        }

        return Promise.reject(new Error(`Unexpected fetch URL: ${url}`));
      });

    render(<App />);

    const applicationSelect = await screen.findByLabelText("Application");

    const activityTypeSelect = screen.getByLabelText("Event Type");

    const notesInput = screen.getByLabelText("Notes");

    fireEvent.change(applicationSelect, {
      target: { value: "7" },
    });

    fireEvent.change(activityTypeSelect, {
      target: { value: "Interview completed" },
    });

    fireEvent.change(notesInput, {
      target: { value: "Second interview completed." },
    });

    fireEvent.click(
      screen.getByRole("button", {
        name: "Record Activity",
      }),
    );

    expect(await screen.findByText("Activity recorded.")).toBeInTheDocument();

    expect(fetchMock).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/activity",
      expect.objectContaining({
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          application_id: 7,
          event_type: "Interview completed",
          notes: "Second interview completed.",
        }),
      }),
    );
  });

  it("shows application activity history when an application is selected", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockImplementation((url) => {
        if (
          url === "http://127.0.0.1:8000/applications/needs-attention" ||
          url === "http://127.0.0.1:8000/activity/today"
        ) {
          return Promise.resolve({
            ok: true,
            json: async () => [],
          } as Response);
        }

        if (url === "http://127.0.0.1:8000/applications") {
          return Promise.resolve({
            ok: true,
            json: async () => [
              {
                application_id: 7,
                job_id: 42,
                status: "APPLIED",
                job_title: "Senior SDET",
                company: "Applied Systems",
              },
            ],
          } as Response);
        }

        if (url === "http://127.0.0.1:8000/activity-types") {
          return Promise.resolve({
            ok: true,
            json: async () => [],
          } as Response);
        }

        if (url === "http://127.0.0.1:8000/applications/7/activity") {
          return Promise.resolve({
            ok: true,
            json: async () => [
              {
                event_id: 101,
                application_id: 7,
                event_type: "Interview completed",
                occurred_at: "2026-08-14T16:00:00+00:00",
                notes: "Second-round interview completed.",
                job_id: 42,
                job_title: "Senior SDET",
                company: "Applied Systems",
              },
            ],
          } as Response);
        }

        return Promise.reject(new Error(`Unexpected fetch URL: ${url}`));
      });

    render(<App />);

    const applicationButton = await screen.findByRole("button", {
      name: "Senior SDET",
    });

    applicationButton.click();

    expect(await screen.findByText("Activity History")).toBeInTheDocument();

    expect(await screen.findByText("Interview completed")).toBeInTheDocument();

    expect(
      screen.getByText("Second-round interview completed."),
    ).toBeInTheDocument();

    expect(fetchMock).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/applications/7/activity",
    );
  });

  it("marks a selected application as rejected", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockImplementation((url, options) => {
        if (
          url === "http://127.0.0.1:8000/applications/needs-attention" ||
          url === "http://127.0.0.1:8000/activity/today"
        ) {
          return Promise.resolve({
            ok: true,
            json: async () => [],
          } as Response);
        }

        if (url === "http://127.0.0.1:8000/activity-types") {
          return Promise.resolve({
            ok: true,
            json: async () => [],
          } as Response);
        }

        if (url === "http://127.0.0.1:8000/applications" && !options) {
          return Promise.resolve({
            ok: true,
            json: async () => [
              {
                application_id: 7,
                job_id: 42,
                status: "APPLIED",
                job_title: "Senior SDET",
                company: "Applied Systems",
              },
            ],
          } as Response);
        }

        if (
          url === "http://127.0.0.1:8000/applications/7/activity" &&
          !options
        ) {
          return Promise.resolve({
            ok: true,
            json: async () => [],
          } as Response);
        }

        if (
          url === "http://127.0.0.1:8000/applications/7/mark-rejected" &&
          options?.method === "POST"
        ) {
          return Promise.resolve({
            ok: true,
            json: async () => ({
              application_id: 7,
              job_id: 42,
              status: "REJECTED",
            }),
          } as Response);
        }

        return Promise.reject(new Error(`Unexpected fetch URL: ${url}`));
      });

    render(<App />);

    const applicationButton = await screen.findByRole("button", {
      name: "Senior SDET",
    });

    applicationButton.click();

    const statusNote = await screen.findByLabelText("Status note");

    fireEvent.change(statusNote, {
      target: {
        value: "Company selected another candidate.",
      },
    });

    fireEvent.click(
      screen.getByRole("button", {
        name: "Mark Rejected",
      }),
    );

    expect(fetchMock).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/applications/7/mark-rejected",
      expect.objectContaining({
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          notes: "Company selected another candidate.",
        }),
      }),
    );
  });

  it("marks a selected application as withdrawn", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockImplementation((url, options) => {
        if (
          url === "http://127.0.0.1:8000/applications/needs-attention" ||
          url === "http://127.0.0.1:8000/activity/today"
        ) {
          return Promise.resolve({
            ok: true,
            json: async () => [],
          } as Response);
        }

        if (url === "http://127.0.0.1:8000/activity-types") {
          return Promise.resolve({
            ok: true,
            json: async () => [],
          } as Response);
        }

        if (url === "http://127.0.0.1:8000/applications" && !options) {
          return Promise.resolve({
            ok: true,
            json: async () => [
              {
                application_id: 7,
                job_id: 42,
                status: "APPLIED",
                job_title: "Senior SDET",
                company: "Applied Systems",
              },
            ],
          } as Response);
        }

        if (
          url === "http://127.0.0.1:8000/applications/7/activity" &&
          !options
        ) {
          return Promise.resolve({
            ok: true,
            json: async () => [],
          } as Response);
        }

        if (
          url === "http://127.0.0.1:8000/applications/7/mark-withdrawn" &&
          options?.method === "POST"
        ) {
          return Promise.resolve({
            ok: true,
            json: async () => ({
              application_id: 7,
              job_id: 42,
              status: "WITHDRAWN",
            }),
          } as Response);
        }

        return Promise.reject(new Error(`Unexpected fetch URL: ${url}`));
      });

    render(<App />);

    const applicationButton = await screen.findByRole("button", {
      name: "Senior SDET",
    });

    applicationButton.click();

    const statusNote = await screen.findByLabelText("Status note");

    fireEvent.change(statusNote, {
      target: {
        value: "Candidate withdrew from consideration.",
      },
    });

    fireEvent.click(
      screen.getByRole("button", {
        name: "Mark Withdrawn",
      }),
    );

    expect(fetchMock).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/applications/7/mark-withdrawn",
      expect.objectContaining({
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          notes: "Candidate withdrew from consideration.",
        }),
      }),
    );
  });

  it("marks a selected application as closed", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockImplementation((url, options) => {
        if (
          url === "http://127.0.0.1:8000/applications/needs-attention" ||
          url === "http://127.0.0.1:8000/activity/today"
        ) {
          return Promise.resolve({
            ok: true,
            json: async () => [],
          } as Response);
        }

        if (url === "http://127.0.0.1:8000/activity-types") {
          return Promise.resolve({
            ok: true,
            json: async () => [],
          } as Response);
        }

        if (url === "http://127.0.0.1:8000/applications" && !options) {
          return Promise.resolve({
            ok: true,
            json: async () => [
              {
                application_id: 7,
                job_id: 42,
                status: "APPLIED",
                job_title: "Senior SDET",
                company: "Applied Systems",
              },
            ],
          } as Response);
        }

        if (
          url === "http://127.0.0.1:8000/applications/7/activity" &&
          !options
        ) {
          return Promise.resolve({
            ok: true,
            json: async () => [],
          } as Response);
        }

        if (
          url === "http://127.0.0.1:8000/applications/7/mark-closed" &&
          options?.method === "POST"
        ) {
          return Promise.resolve({
            ok: true,
            json: async () => ({
              application_id: 7,
              job_id: 42,
              status: "CLOSED",
            }),
          } as Response);
        }

        return Promise.reject(new Error(`Unexpected fetch URL: ${url}`));
      });

    render(<App />);

    const applicationButton = await screen.findByRole("button", {
      name: "Senior SDET",
    });

    applicationButton.click();

    const statusNote = await screen.findByLabelText("Status note");

    fireEvent.change(statusNote, {
      target: {
        value: "Application closed.",
      },
    });

    fireEvent.click(
      screen.getByRole("button", {
        name: "Mark Closed",
      }),
    );

    expect(fetchMock).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/applications/7/mark-closed",
      expect.objectContaining({
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          notes: "Application closed.",
        }),
      }),
    );
  });
});
