//
//  ElementQueryCreator.swift
//  MobiliumDriver
//
//  Created by Tomasz Oraczewski on 07/11/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

import MobiliumFramework
import XCTest

class ElementQueryCreator {

    static func create(from xpath: String, provider: XCUIElementTypeQueryProvider) -> XCUIElementQuery? {
        let paths = XPathParser.parse(xpath)
        var query: XCUIElementQuery?
        for path in paths {
            let provider: XCUIElementTypeQueryProvider = query ?? provider
            query = elementTypeQuery(from: path.elementType, provider: provider)
            if let condition = path.condition,
                let currentQuery = query {
                query = conditionQuery(from: condition, query: currentQuery)
            }
        }
        return query
    }

    private static func elementTypeQuery(from elementType: Path.ElementType,
                                         provider: XCUIElementTypeQueryProvider) -> XCUIElementQuery {
        switch elementType {
        case .cell:
            return provider.cells
        case .button:
            return provider.buttons
        case .navigationBar:
            return provider.navigationBars
        case .textField:
            return provider.textFields
        case .textView:
            return provider.textViews
        case .switchButton:
            return provider.switches
        }
    }

    private static func conditionQuery(from condition: PathCondition,
                                       query: XCUIElementQuery) -> XCUIElementQuery? {
        guard case .contains = condition.type else { return nil }

        let rawPredicate = "\(condition.parameterType.rawValue) CONTAINS '\(condition.value)'"
        let predicate = NSPredicate(format: rawPredicate)
        return query.matching(predicate)
    }
}
