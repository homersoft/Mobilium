//
//  XPathParser.swift
//  MobiliumDriver
//
//  Created by Tomasz Oraczewski on 06/11/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

import Foundation

class XPathParser {
    static let xPathRegex = "(\\w+)(?:(?:\\[(\\w+)\\(@(\\w+),\\s*'([\\w|\\d]+)'\\)\\])?)"

    static func parse(_ xpath: String) -> [Path] {
        let groups = XPathParser.groups(of: xpath, for: xPathRegex)
        return groups.compactMap(path(from:))
    }

    private static func path(from group: [String]) -> Path? {
        guard group.count>=1 else { return nil }

        let rawElementType = group[1]
        guard let elementType = elementType(raw: rawElementType) else { return nil }

        return Path(elementType: elementType, condition: condition(from: group))
    }

    private static func condition(from group: [String]) -> PathCondition? {
        guard group.count >= 5,
        let conditionType = conditionType(raw: group[2]),
        let parameterType = parameterType(raw: group[3]) else { return nil }

        return PathCondition(type: conditionType, parameterType: parameterType, value: group[4])
    }

    private static func elementType(raw: String) -> Path.ElementType? {
        switch raw {
        case "XCUIElementTypeCell":
            return .cell
        case "XCUIElementTypeButton":
            return .button
        default:
            return nil
        }
    }

    private static func conditionType(raw: String) -> PathCondition.ConditionType? {
        switch raw {
        case "contains":
            return .contains
        default:
            return nil
        }
    }

    private static func parameterType(raw: String) -> PathCondition.ParameterType? {
        switch raw {
        case "label":
            return .label
        default:
            return nil
        }
    }

    private static func groups(of text: String, for regexPattern: String) -> [[String]] {
        let regex = try? NSRegularExpression(pattern: regexPattern)
        guard let matches = regex?.matches(in: text, range: NSRange(text.startIndex..., in: text)) else { return [] }

        return matches.map { match in
            return (0..<match.numberOfRanges).compactMap {
                let rangeBounds = match.range(at: $0)
                guard let range = Range(rangeBounds, in: text) else { return nil }

                return String(text[range])
            }
        }
    }
}

struct Path: Equatable {
    let elementType: ElementType
    let condition: PathCondition?

    init(elementType: ElementType, condition: PathCondition? = nil) {
        self.elementType = elementType
        self.condition = condition
    }

    enum ElementType {
        case cell
        case button
    }
}

struct PathCondition: Equatable {
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
