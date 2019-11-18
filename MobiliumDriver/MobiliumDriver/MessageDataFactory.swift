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

    static func isElementVisibleResponse(accessibility: Accessibility, exists: Bool) -> Data {
        return dataWith(populator: { populator in
            var response = IsElementVisibleResponse()
            response.isVisible = exists
            response.elementIndicator = accessibility.toElementIdicator()
            populator.message = .isElementVisibleResponse(response)
        })
    }
    
    static func clickElementResponse(accessibility: Accessibility, exists: Bool) -> Data {
        return dataWith(populator: { populator in
            var response = ClickElementResponse()
            response.elementIndicator = accessibility.toElementIdicator()
            response.status = exists ? .success(true) : .failure(.elementNotExists)
            populator.message = .clickElementResponse(response)
        })
    }
    
    static func getValueOfElementResponse(accessibility: Accessibility, exists: Bool, value: String?) -> Data {
        return dataWith(populator: { populator in
            var response = GetValueOfElementResponse()
            response.elementIndicator = accessibility.toElementIdicator()
            if exists {
                response.status = .value(value ?? "")
            } else {
                response.status = .failure(.elementNotExists)
            }
            populator.message = .getValueOfElementResponse(response)
        })
    }

    static func setValueOfElementResponse(accessibility: Accessibility, exists: Bool) -> Data {
        return dataWith(populator: { populator in
            var response = SetValueOfElementResponse()
            response.elementIndicator = accessibility.toElementIdicator()
            response.status = exists ? .success(true) : .failure(.elementNotExists)
            populator.message = .setValueOfElementResponse(response)
        })
    }

    static func getElementsCountResponse(accessibility: Accessibility, count: Int) -> Data {
        return dataWith(populator: { populator in
            var response = GetElementsCountResponse()
            response.elementIndicator = accessibility.toElementIdicator()
            response.count = Int64(count)
            populator.message = .getElementsCountResponse(response)
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
