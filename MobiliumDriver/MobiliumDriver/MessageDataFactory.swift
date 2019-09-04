//
//  MessageFactory.swift
//  MobiliumDriver
//
//  Created by Tomasz Oraczewski on 26/07/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

import Foundation

class MessageDataFactory {

    static func startDriverResponse() -> Data {
        return dataWith { populator in
            populator.message = .startDriverResponse(StartDriverResponse())
        }
    }

    static func appLaunchResponse() -> Data {
        return dataWith(populator: { populator in
            populator.message = .launchAppResponse(LaunchAppResponse())
        })
    }

    static func isElementVisibleResponse(accessibilityId: String, isVisible: Bool) -> Data {
        return dataWith(populator: { populator in
            var response = IsElementVisibleResponse()
            response.isVisible = isVisible
            response.accessibilityID = accessibilityId
            populator.message = .isElementVisibleResponse(response)
        })
    }
    
    static func clickElementResponse(accessibilityId: String) -> Data {
        return dataWith(populator: { populator in
            var response = ClickElementResponse()
            response.accessibilityID = accessibilityId
            populator.message = .clickElementResponse(response)
        })
    }

    static func terminateAppResponse() -> Data {
        return dataWith(populator: { populator in
            let response = TerminateAppResponse()
            populator.message = .terminateAppResponse(response)
        })
    }

    static private func dataWith(populator: (inout MobiliumMessage) throws -> ()) -> Data {
        guard let message = try? MobiliumMessage.with(populator),
            let data = try? message.serializedData() else { return Data() }

        return data
    }
}
