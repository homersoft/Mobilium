//
//  XPathParser.swift
//  MobiliumDriver
//
//  Created by Tomasz Oraczewski on 06/11/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

import Foundation

class XPathParser {
    static func parse(_ xpath: String) -> [Path] {
        return []
    }
}

struct Path {
    let elementType: ElementType
    let condition: PathCondition?

    enum ElementType {
        case cell
        case button
    }
}

struct PathCondition {
    let type: ConditionType
    let parameterType: ParameterType
    let value: String

    enum ParameterType {
        case label
    }

    enum ConditionType {
        case contains
    }
}
