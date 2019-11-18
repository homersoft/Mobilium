//
//  Accessibility.swift
//  MobiliumDriver
//
//  Created by Tomasz Oraczewski on 05/11/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

import Foundation

enum Accessibility {
    case id(String)
    case xpath(String)
}

extension Accessibility {
    var id: String? {
        guard case let .id(accessibilityId) = self else { return nil }

        return accessibilityId
    }
}

extension Accessibility {
    func toElementIndicator() -> ElementIndicator{
        var elementIdicator = ElementIndicator()
        switch self {
        case .id(let accessibilityId):
            elementIdicator.id = accessibilityId
        case .xpath(let xpath):
            elementIdicator.xpath = xpath
        }
        return elementIdicator
    }
}

extension ElementIndicator {
    func toAccessibility() -> Accessibility? {
        switch self.type {
        case .id(let accessibilityId):
            return .id(accessibilityId)
        case .xpath(let xpath):
            return .xpath(xpath)
        default:
            return nil
        }
    }
}
