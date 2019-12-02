//
//  MobiliumDriver.swift
//  MobiliumDriver
//
//  Created by Marek Niedbach on 21/05/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

import XCTest
import Network
import SocketIO
import MobiliumFramework

class MobiliumDriver: XCTestCase, StreamDelegate {
    var app: XCUIApplication!
    var socket: SocketIOClient?
    var deserializer = MessageDeserializer()
    var keepAlive = true

    func testApplication() {
        guard let host = ProcessInfo.processInfo.environment["HOST"],
            let port = ProcessInfo.processInfo.environment["PORT"] else { return XCTFail("Host or port not provided") }

        let manager = SocketManager(socketURL: URL(string: "tcp://\(host):\(port)")!, config: [.log(true), .compress])
        socket = manager.socket(forNamespace: "/driver")

        socket?.on(clientEvent: .connect) { [weak self] (data, ack) in
            print("Driver socket connected!")
            let data = MessageDataFactory.startDriverResponse()
            self?.socket?.send(message: data)
        }
        socket?.on(clientEvent: .disconnect) { [weak self] (data, ack) in
            print("Driver socket disconnected!")
            self?.keepAlive = false
        }
        socket?.on("message") { [weak self] (data, ack) in
            print("Driver did receive message")
            guard let data = data as? [Data] else { return }

            if let message = self?.deserializer.launchAppRequest(from: data) {
                self?.launchApp(bundleId: message.bundleID)
            }

            if let message = self?.deserializer.isElementVisibileRequest(from: data),
                let accessibility = message.elementIndicator.toAccessibility() {
                self?.checkElementVisible(with: accessibility, at: Int(message.index),
                                          timeout: TimeInterval(message.timeout))
            }
            
            if let message = self?.deserializer.isElementInvisibileRequest(from: data),
                let accessibility = message.elementIndicator.toAccessibility() {
                self?.checkElementInvisible(with: accessibility, at: Int(message.index),
                                            timeout: TimeInterval(message.timeout))
            }

            if let message = self?.deserializer.isElementEnabledRequest(from: data),
                let accessibility = message.elementIndicator.toAccessibility() {
                self?.checkElementEnabled(with: accessibility, at: Int(message.index))
            }
            
            if let message = self?.deserializer.getValueOfElementRequest(from: data),
                let accessibility = message.elementIndicator.toAccessibility() {
                self?.readValueOfElement(with: accessibility, at: Int(message.index))
            }
            
            if let message = self?.deserializer.setValueOfElementRequest(from: data) {
                self?.setValueOfElementUsingMessage(message, at: Int(message.index))
            }
            
            if let message = self?.deserializer.clickElementRequest(from: data),
                let accessibility = message.elementIndicator.toAccessibility() {
                self?.clickElement(with: accessibility, at: Int(message.index))
            }

            if let message = self?.deserializer.getElementsCountRequest(from: data) {
                self?.getElementsCountUsingMessage(message)
            }
            
            if let _ = self?.deserializer.terminateAppRequest(from: data) {
                self?.terminateApp()
            }
        }
        print("Driver socket connection attempt")
        socket?.connect()

        while keepAlive && RunLoop.main.run(mode: .default, before: .distantFuture) { }
    }

    private func launchApp(bundleId: String) {
        continueAfterFailure = true

        app = XCUIApplication(bundleIdentifier: bundleId)
        app.launch()

        addUIInterruptionMonitor(withDescription: "BT permissisons alert monitor") { alert in
            if alert.buttons["OK"].exists {
                alert.buttons["OK"].tap()
                return true
            }
            return false
        }

        Thread.sleep(forTimeInterval: 1.0)

        let data = MessageDataFactory.appLaunchResponse()
        socket?.send(message: data)
    }

    private func terminateApp() {
        app.terminate()

        let messageData = MessageDataFactory.terminateAppResponse()
        socket?.send(message: messageData)
    }

    private func checkElementVisible(with accessibility: Accessibility, at index: Int, timeout: TimeInterval) {
        let element = self.element(by: accessibility, at: index)
        let elementExists = element?.waitForExistence(timeout: timeout) ?? false

        let messageData = MessageDataFactory.isElementVisibleResponse(accessibility: accessibility,
                                                                      exists: elementExists)
        socket?.send(message: messageData)
    }
    
    private func checkElementInvisible(with accessibility: Accessibility, at index: Int, timeout: TimeInterval) {
        let predicate = NSPredicate { object, _ in
             (object as? XCUIElement)?.exists == false
        }
        let element = self.element(by: accessibility, at: index)
        let exp = expectation(for: predicate, evaluatedWith: element, handler: nil)
        
        wait(for: [exp], timeout: timeout)
        
        let elementExists = element?.exists ?? false
        let messageData = MessageDataFactory.isElementInvisibleResponse(accessibility: accessibility,
                                                                        exists: elementExists)
        socket?.send(message: messageData)
    }

    private func checkElementEnabled(with accessibility: Accessibility, at index: Int) {
        let element = self.element(by: accessibility, at: index)
        let elementEnabled = element?.isEnabled ?? false

        let messageData = MessageDataFactory.isElementEnabledResponse(accessibility: accessibility,
                                                                      enabled: elementEnabled)
        socket?.send(message: messageData)
    }
    
    private func clickElement(with accessibility: Accessibility, at index: Int) {
        let element = self.element(by: accessibility, at: index)
        let elementExists = element?.exists ?? false
        if elementExists {
            element?.tap()
        }
        
        let messageData = MessageDataFactory.clickElementResponse(accessibility: accessibility, exists: elementExists)
        socket?.send(message: messageData)
    }
    
    private func readValueOfElement(with accessibility: Accessibility, at index: Int) {
        let element = self.element(by: accessibility, at: index)
        guard element?.exists == true else {
            let messageData = MessageDataFactory.getValueOfElementResponse(accessibility: accessibility,
                                                                           exists: false, value: nil)
            socket?.send(message: messageData)
            return
        }

        let value = element?.value as? String ?? element?.label
        let messageData = MessageDataFactory.getValueOfElementResponse(accessibility: accessibility,
                                                                       exists: true, value: value)
        socket?.send(message: messageData)
    }
    
    private func setValueOfElementUsingMessage(_ message: SetValueOfElementRequest, at index: Int) {
        guard let accessibility = message.elementIndicator.toAccessibility() else { return }

        let element = self.element(by: accessibility, at: index)
        guard element?.exists == true else {
            let messageData = MessageDataFactory.setValueOfElementResponse(accessibility: accessibility,
                                                                           exists: false)
            socket?.send(message: messageData)
            return
        }

        switch message.value {
        case .text(let newTextValue)?:
            element?.setText(newTextValue.value, replace: newTextValue.clears)
        case .position(let newPosition)?:
            element?.adjust(toNormalizedSliderPosition: CGFloat(newPosition))
        case .selection(let newValue)?:
            element?.setSelection(to: newValue)
        default:
            print("Invalid message send to driver. Message: \(String(describing: message))")
        }
        
        let messageData = MessageDataFactory.setValueOfElementResponse(accessibility: accessibility,
                                                                       exists: true)
        socket?.send(message: messageData)
    }

    private func getElementsCountUsingMessage(_ message: GetElementsCountRequest) {
        guard let accessibility = message.elementIndicator.toAccessibility() else { return }

        let elements = self.elementQuery(by: accessibility)
        let count = elements?.count ?? 0

        let response = MessageDataFactory.getElementsCountResponse(accessibility: accessibility, count: count)
        socket?.send(message: response)
    }

    private func element(by accessibility: Accessibility, at index: Int) -> XCUIElement? {
        switch accessibility {
        case .id(let accessibilityId):
            return app.element(with: accessibilityId, index: index)
        case .xpath(let xpath):
            guard let query = ElementQueryCreator.create(from: xpath, provider: app) else {
                print("Cannot build query from xpath!")
                return nil
            }

            return query.element(boundBy: index)
        }
    }

    private func elementQuery(by accessibility: Accessibility) -> XCUIElementQuery? {
        switch accessibility {
        case .id(let accessibilityId):
            return app.descendants(matching: .any).matching(identifier: accessibilityId)
        case .xpath(let xpath):
            guard let query = ElementQueryCreator.create(from: xpath, provider: app) else {
                print("Cannot build query from xpath!")
                return nil
            }
            return query
        }
    }
}
