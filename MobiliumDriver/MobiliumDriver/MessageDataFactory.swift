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

    static func isElementVisibleResponse(accessibilityId: String, exists: Bool) -> Data {
        return dataWith(populator: { populator in
            var response = IsElementVisibleResponse()
            response.isVisible = exists
            response.accessibilityID = accessibilityId
            populator.message = .isElementVisibleResponse(response)
        })
    }
    
    static func clickElementResponse(accessibilityId: String, exists: Bool) -> Data {
        return dataWith(populator: { populator in
            var response = ClickElementResponse()
            response.accessibilityID = accessibilityId
            response.status = exists ? .success(true) : .failure(ElementNotExists())
            populator.message = .clickElementResponse(response)
        })
    }
    
    static func getValueOfElementResponse(accessibilityId: String, value: String?) -> Data {
        return dataWith(populator: { populator in
            var response = GetValueOfElementResponse()
            response.accessibilityID = accessibilityId
            if let value = value {
                response.status = .value(value)
            } else {
                response.status = .failure(ElementNotExists())
            }
            populator.message = .getValueOfElementResponse(response)
        })
    }

    static func setValueOfElementResponse(accessibilityId: String, exists: Bool) -> Data {
        return dataWith(populator: { populator in
            var response = SetValueOfElementResponse()
            response.accessibilityID = accessibilityId
            response.status = exists ? .success(true) : .failure(ElementNotExists())
            populator.message = .setValueOfElementResponse(response)
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
