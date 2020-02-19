//
//  MessageDeserializer.swift
//  MobiliumDriver
//
//  Created by Tomasz Oraczewski on 26/07/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

import Foundation
import SwiftProtobuf

class MessageDeserializer {
    func launchAppRequest(from data: [Data]) -> LaunchAppRequest? {
        let message = extract(from: data) { oneOfMessage in
            guard case .launchAppRequest(let message) = oneOfMessage else { return nil }

            return message
        }
        return message as? LaunchAppRequest
    }

    func touchRequest(from data: [Data]) -> TouchRequest? {
        let message = extract(from: data) { oneOfMessage in
            guard case .touchRequest(let message) = oneOfMessage else { return nil }

            return message
        }
        return message as? TouchRequest
    }

    func getWindowSizeRequest(from data: [Data]) -> GetWindowSizeRequest? {
        let message = extract(from: data) { oneOfMessage in
            guard case .getWindowSizeRequest(let message) = oneOfMessage else { return nil }

            return message
        }
        return message as? GetWindowSizeRequest
    }

    func isElementVisibileRequest(from data: [Data]) -> IsElementVisibleRequest? {
        let message = extract(from: data) { oneOfMessage in
            guard case .isElementVisibleRequest(let message) = oneOfMessage else { return nil }

            return message
        }
        return message as? IsElementVisibleRequest
    }
    
    func isElementInvisibileRequest(from data: [Data]) -> IsElementInvisibleRequest? {
        let message = extract(from: data) { oneOfMessage in
            guard case .isElementInvisibleRequest(let message) = oneOfMessage else { return nil }

            return message
        }
        return message as? IsElementInvisibleRequest
    }

    func isElementEnabledRequest(from data: [Data]) -> IsElementEnabledRequest? {
        let message = extract(from: data) { oneOfMessage in
            guard case .isElementEnabledRequest(let message) = oneOfMessage else { return nil }

            return message
        }
        return message as? IsElementEnabledRequest
    }

    func terminateAppRequest(from data: [Data]) -> TerminateAppRequest? {
        let message = extract(from: data) { oneOfMessage in
            guard case .terminateAppRequest(let message) = oneOfMessage else { return nil }

            return message
        }
        return message as? TerminateAppRequest
    }
    
    func clickElementRequest(from data: [Data]) -> ClickElementRequest? {
        let message = extract(from: data) { oneOfMessage in
            guard case .clickElementRequest(let message) = oneOfMessage else { return nil }
            
            return message
        }
        return message as? ClickElementRequest
    }
    
    func getValueOfElementRequest(from data: [Data]) -> GetValueOfElementRequest? {
        let message = extract(from: data) { oneOfMessage in
            guard case .getValueOfElementRequest(let message) = oneOfMessage else { return nil }
            
            return message
        }
        return message as? GetValueOfElementRequest
    }

    func setValueOfElementRequest(from data: [Data]) -> SetValueOfElementRequest? {
        let message = extract(from: data) { oneOfMessage in
            guard case .setValueOfElementRequest(let message) = oneOfMessage else { return nil }
            
            return message
        }
        return message as? SetValueOfElementRequest
    }

    func getElementsCountRequest(from data: [Data]) -> GetElementsCountRequest? {
        let message = extract(from: data) { oneOfMessage in
            guard case .getElementsCountRequest(let message) = oneOfMessage else { return nil }

            return message
        }
        return message as? GetElementsCountRequest
    }
    
    func getElementIdRequest(from data: [Data]) -> GetElementIdRequest? {
        let message = extract(from: data) { oneOfMessage in
            guard case .getElementIDRequest(let message) = oneOfMessage else { return nil }
            
            return message
        }
        return message as? GetElementIdRequest
    }
    
    private func extract(from data: [Data], using extractor: (MobiliumMessage.OneOf_Message) -> Message?) -> Message? {
        guard let serializedData = data.first,
            let mobiliumMessage = try? MobiliumMessage(serializedData: serializedData),
            let oneOfMessage = mobiliumMessage.message else { return nil }

        return extractor(oneOfMessage)
    }
}
