//
//  XPathParser.swift
//  MobiliumDriver
//
//  Created by Tomasz Oraczewski on 06/11/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

import Foundation

public class XPathParser {
    private static let xPathRegex = "(\\w+)(?:(?:\\[(\\w+)\\(@(\\w+),\\s*'([^']+)'\\)\\])?)"

    public static func parse(_ xpath: String) -> [Path] {
        let groups = self.groups(of: xpath, for: xPathRegex)
        return groups.compactMap(path(from:))
    }

    private static func path(from group: [String]) -> Path? {
        guard group.count > 1 else { return nil }

        let xpathElement = group[1]
        guard let elementType = Path.ElementType(xpathElement: xpathElement) else { return nil }

        return Path(elementType: elementType, condition: condition(from: group))
    }

    private static func condition(from group: [String]) -> PathCondition? {
        guard group.count >= 5,
            let conditionType = PathCondition.ConditionType(xpathCondition: group[2]),
            let parameterType = PathCondition.ParameterType(xpathParameter: group[3]) else { return nil }

        return PathCondition(type: conditionType, parameterType: parameterType, value: group[4])
    }

    private static func groups(of text: String, for regexPattern: String) -> [[String]] {
        let regex = try? NSRegularExpression(pattern: regexPattern)
        guard let matches = regex?.matches(in: text, range: NSRange(text.startIndex..., in: text)) else { return [] }

        return matches.map { group(in: $0, of: text) }
    }

    private static func group(in match: NSTextCheckingResult, of text: String) -> [String] {
        return (0..<match.numberOfRanges).compactMap { groupResult(at: $0, in: match, of: text) }
    }

    private static func groupResult(at index: Int, in match: NSTextCheckingResult, of text: String) -> String? {
        let rangeBounds = match.range(at: index)
        guard let range = Range(rangeBounds, in: text) else { return nil }

        return String(text[range])
    }
}

private extension Path.ElementType {
    init?(xpathElement: String) {
        switch xpathElement {
        case "XCUIElementTypeCell":
            self = .cell
        case "XCUIElementTypeButton":
            self = .button
        case "XCUIElementTypeNavigationBar":
            self = .navigationBar
        case "XCUIElementTypeTextField":
            self = .textField
        case "XCUIElementTypeTextView":
            self = .textView
        case "XCUIElementTypeSwitch":
            self = .switchButton
        default:
            return nil
        }
    }
}

private extension PathCondition.ConditionType {
    init?(xpathCondition: String) {
        switch xpathCondition {
        case "contains":
            self = .contains
        default:
            return nil
        }
    }
}

private extension PathCondition.ParameterType {
    init?(xpathParameter: String) {
        switch xpathParameter {
        case "label":
            self = .label
        case "value":
            self = .value
        default:
            return nil
        }
    }
}
