//
//  SocketIOClient+SendMessage.swift
//  MobiliumDriver
//
//  Created by Grzegorz Przybyła on 16/09/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

import Foundation
import SocketIO
import XCTest

extension SocketIOClient {
    func send(message data: Data) {
        let deadline = Date(timeIntervalSinceNow: 30)
        waitForConnection(until: deadline, success: { [weak self] in
            self?.emit("message", with: [data])
        }, failure: { [weak self] in
            self?.failDriver()
        })
    }

    private func waitForConnection(until deadline: Date, success: @escaping () -> (), failure: @escaping () ->()) {
        if isConnected() {
            success()
        } else if deadline.timeIntervalSinceNow < 0 {
            failure()
        } else {
            print("Driver is waiting for connection with server...")
            DispatchQueue.main.asyncAfter(deadline: .now() + 1) { [weak self] in
                self?.waitForConnection(until: deadline, success: success, failure: failure)
            }
        }
    }

    private func isConnected() -> Bool {
        return self.status == .connected
    }

    private func failDriver() {
        XCTFail("Driver reconnection failed!")
    }
}
