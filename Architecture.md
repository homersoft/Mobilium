# Mobilium framework architecture

#### Components
- **Mobilium Server** - the core of the Mobilium project. This application written in python is a gate for communication between Client and Driver. In addition, the Server is responsible for running MobiliumDriver on device/simulator.
- **Mobilium iOS Driver** - UI Test executor. This component has an implementation of our testing procedures, and it is run on the iOS device. It is directly testing System Under Test (SUT), which will be your iOS application.
- **Mobilium Client** - UI Test runner where we manage whole testing process, request application and environment changes on the server and communicate through the system with SUT

![Diagram](artifacts/sut.png)

#### Components communication
We used WebSockets to allow communication between components. WebSockets ensure quick, reliable two-way communication.
The following diagram represents how communication flow is achieved. An important note is that, the client is never directly sending messages to the iOS driver, instead client sends a request to the server, which will be decided if this request should be handled by the server or proceed to the driver directly.

![DataFlow](artifacts/data_flow_diagram.png)

#### Proto models

All communication between components is based on request/response model.
This means that at the time, there is only one request performed by client, and client is waiting for a response dedicated for that request. This request can be handled by server or proxied to the iOS driver.
When request is handled server is sending or proxying response to the client.

To unify all messages (request/response) we've decided to use [Google proto](https://developers.google.com/protocol-buffers).

All framework components are using one, shared proto models. Those models are defined inside `proto/messages.proto`.

For Client/Server we are using messages generated for python.
iOS driver is using Swift proto message definitions
