//
//  Accessibility.swift
//  MobiliumDriver
//
//  Created by Tomasz Oraczewski on 05/11/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

import Foundation

enum Accessibility {
    case id(value: String)
    case xpath(value: String)
}

extension Accessibility {
    var id: String? {
        guard case let .id(value) = self else { return nil }

        return value
    }
}

extension Accessibility {
    func toElementIdicator() -> ElementIndicator{
        var elementIdicator = ElementIndicator()
        switch self {
        case .id(let value):
            elementIdicator.id = value
        case .xpath(let value):
            elementIdicator.xpath = value
        }
        return elementIdicator
    }
}

extension ElementIndicator {
    func toAccessibility() -> Accessibility? {
        switch self.type {
        case .id(let value):
            return .id(value: value)
        case .xpath(let value):
            return .xpath(value: value)
        default:
            return nil
        }
    }
}
