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

    func checkElementVisibility(from data: [Data]) -> CheckElementVisibleRequest? {
        let message = extract(from: data) { oneOfMessage in
            guard case .checkElementVisibleRequest(let message) = oneOfMessage else { return nil }

            return message
        }
        return message as? CheckElementVisibleRequest
    }

    func launchAppRequest(from data: [Data]) -> LaunchAppRequest? {
        let message = extract(from: data) { oneOfMessage in
            guard case .launchAppRequest(let message) = oneOfMessage else { return nil }

            return message
        }
        return message as? LaunchAppRequest
    }

    private func extract(from data: [Data], using extractor: (MobiliumMessage.OneOf_Message) -> Message?) -> Message? {
        guard let serializedData = data.first,
            let mobiliumMessage = try? MobiliumMessage(serializedData: serializedData),
            let oneOfMessage = mobiliumMessage.message else { return nil }

        return extractor(oneOfMessage)
    }
}
