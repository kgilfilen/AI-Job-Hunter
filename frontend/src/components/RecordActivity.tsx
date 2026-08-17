export type TrackedApplication = {
  application_id: number;
  job_id: number;
  status: string;
  job_title: string | null;
  company: string | null;
};

export type ActivityForm = {
  application_id: string;
  event_type: string;
  notes: string;
};

type RecordActivityProps = {
  trackedApplications: TrackedApplication[];
  activityTypes: string[];
  activityForm: ActivityForm;
  submitMessage: string | null;
  onFormChange: (form: ActivityForm) => void;
  onSubmit: (event: React.FormEvent<HTMLFormElement>) => void;
};

export function RecordActivity({
  trackedApplications,
  activityTypes,
  activityForm,
  submitMessage,
  onFormChange,
  onSubmit,
}: RecordActivityProps) {
  return (
    <>
      <h2>Record Activity</h2>

      <form onSubmit={onSubmit}>
        <div>
          <label>
            Application
            <select
              value={activityForm.application_id}
              onChange={(event) =>
                onFormChange({
                  ...activityForm,
                  application_id: event.target.value,
                })
              }
              required
            >
              <option value="">Select an application</option>

              {trackedApplications.map((application) => (
                <option
                  key={application.application_id}
                  value={application.application_id}
                >
                  {application.job_title ?? `Job ${application.job_id}`}
                  {application.company ? ` — ${application.company}` : ""}
                  {` (${application.status})`}
                </option>
              ))}
            </select>
          </label>
        </div>
        <div>
          <label>
            Event Type
            <select
              value={activityForm.event_type}
              onChange={(event) =>
                onFormChange({
                  ...activityForm,
                  event_type: event.target.value,
                })
              }
              required
            >
              <option value="">Select an activity type</option>

              {activityTypes.map((activityType) => (
                <option key={activityType} value={activityType}>
                  {activityType}
                </option>
              ))}
            </select>
          </label>
        </div>
        <div>
          <label>
            Notes
            <textarea
              value={activityForm.notes}
              onChange={(event) =>
                onFormChange({
                  ...activityForm,
                  notes: event.target.value,
                })
              }
            />
          </label>
        </div>
        <button type="submit">Record Activity</button>
      </form>

      {submitMessage && <p>{submitMessage}</p>}
    </>
  );
}
