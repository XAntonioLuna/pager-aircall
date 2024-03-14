# pager-aircall

## Description
This is a simple pager application example, it can't run on a real environment, but it is an example of 
how such a system would be modeled and tested.

![Architecture of the Alert Notification System](architecture-diagram.png)

## Requirements
For the tests to run properly you need **Python 3.7+** the main reason is the usage of the `@dataclass` decorator to 
reduce the amount of boilerplate code.

I recommend creating a virtual environment and installing the required dependencies in it. To do so run:

- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`

## Running the tests
To run all tests simpley execute
- `source venv/bin/activate`
- `python -m pytest tests/`

You can also jus run a subset of the tests by changing the `tests` folder to, for example `tests/e2e`

## Design considerations

### Core Domain Model
You can find each one of these models in the `models`  directory
- MonitoredService: Represents a monitored system component. Tracks its current status (Healthy/Unhealthy) and references an escalation policy that should be recovered from the EP service.
- EscalationPolicy: Defines the escalation policy. It's main component being an ordered sequence of Levels.
- Level: A step in the escalation, containing a list of Targets.
- Target: Individual or service to notify (email or SMS).
- Alert: A signal associated with a MonitoredService indicating a problem.
- Notification: Represents a single notification sent to a Level.

### Key Logic
The key logic described below is contained in the `services` directory. Mostly in the `PagerService` class but also in the `NotificationService` class.

- Alert Processing: When an Alert is received, the MonitoredService state is set to Unhealthy, and the EscalationPolicy is used to determine initial notifications.
- Timeout Handling: A 15-minute timer manages escalations. Expiry triggers notifications to the next Level of the EscalationPolicy.
- Acknowledgements: Acknowledgements halt escalations.
- Resolutions: When an alert is marked as resolved, the MonitoredService state is set to Healthy, and escalations are stopped.

### Database Considerations

While not implemented, the design anticipates a relational database. Key considerations include:

#### Tables
Entities would likely map to tables (e.g., MonitoredService, EscalationPolicy, etc.) with appropriate foreign keys.

#### Concurrency & Data consistency
This system prioritizes data consistency by utilizing synchronous database writes, ensuring that the state of a MonitoredService is always accurately reflected, even in a concurrent environment.

The logic checks for the health of the monitored service before triggering new notifications or generating new alerts. This means that once a service is marked as unhealthy, no new alerts will be triggered until it's marked healthy again. The tradoff here is the system only allows for one active alert at the same time for each service.

Some potential scenarios that could arise and are not handled in this example logic include:

- Multiple alerts being triggered for the same service before it's marked as unhealthy. Based on the database assumption both of them couldn't mark the service as unhealthy at the same time and one would fail
- There are no retries for pretty much anything, if a notification fails it's not retried, if the database fails to update the state of a service it's not retried, etc.

### Extensibility

The design could be extended to support:

- Additional Notification Channels: Webhooks, etc.
- Incident History: Tracking past alerts, escalations, and resolutions.
