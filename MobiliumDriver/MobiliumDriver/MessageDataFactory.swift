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

    static func touchResponse() -> Data {
        return dataWith(populator: { populator in
            populator.message = .touchResponse(TouchResponse())
        })
    }

    static func getWindowSizeResponse(width: Float, height: Float) -> Data {
        return dataWith(populator: { populator in
            var response = GetWindowSizeResponse()
            response.width = width
            response.height = height
            populator.message = .getWindowSizeResponse(response)
        })
    }

    static func isElementVisibleResponse(accessibility: Accessibility, exists: Bool) -> Data {
        return dataWith(populator: { populator in
            var response = IsElementVisibleResponse()
            response.isVisible = exists
            response.elementIndicator = accessibility.toElementIndicator()
            populator.message = .isElementVisibleResponse(response)
        })
    }
    
    static func isElementInvisibleResponse(accessibility: Accessibility, exists: Bool) -> Data {
        return dataWith(populator: { populator in
            var response = IsElementInvisibleResponse()
            response.isInvisible = !exists
            response.elementIndicator = accessibility.toElementIndicator()
            populator.message = .isElementInvisibleResponse(response)
        })
    }

    static func isElementEnabledResponse(accessibility: Accessibility, enabled: Bool?) -> Data {
        return dataWith(populator: { populator in
            var response = IsElementEnabledResponse()
            if let enabled = enabled {
                response.status = .isEnabled(enabled)
            } else {
                response.status = .failure(.elementNotExists)
            }
            response.elementIndicator = accessibility.toElementIndicator()
            populator.message = .isElementEnabledResponse(response)
        })
    }
    
    static func clickElementResponse(accessibility: Accessibility, exists: Bool) -> Data {
        return dataWith(populator: { populator in
            var response = ClickElementResponse()
            response.elementIndicator = accessibility.toElementIndicator()
            response.status = exists ? .success(true) : .failure(.elementNotExists)
            populator.message = .clickElementResponse(response)
        })
    }
    
    static func getValueOfElementResponse(accessibility: Accessibility, exists: Bool, value: String?) -> Data {
        return dataWith(populator: { populator in
            var response = GetValueOfElementResponse()
            response.elementIndicator = accessibility.toElementIndicator()
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
            response.elementIndicator = accessibility.toElementIndicator()
            response.status = exists ? .success(true) : .failure(.elementNotExists)
            populator.message = .setValueOfElementResponse(response)
        })
    }

    static func getElementsCountResponse(accessibility: Accessibility, count: Int) -> Data {
        return dataWith(populator: { populator in
            var response = GetElementsCountResponse()
            response.elementIndicator = accessibility.toElementIndicator()
            response.count = Int64(count)
            populator.message = .getElementsCountResponse(response)
        })
    }
    
    static func getElementIdResponse(accessibility: Accessibility, exists: Bool, id: String?) -> Data {
        return dataWith(populator: { populator in
            var response = GetElementIdResponse()
            response.elementIndicator = accessibility.toElementIndicator()
            response.status = exists ? .id(id ?? "") : .failure(.elementNotExists)
            populator.message = .getElementIDResponse(response)
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
