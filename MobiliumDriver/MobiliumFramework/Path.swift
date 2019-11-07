//
//  Path.swift
//  MobiliumFramework
//
//  Created by Tomasz Oraczewski on 07/11/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

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
        case navigationBar
        case textView
        case switchButton
    }
}

struct PathCondition: Equatable {
    let type: ConditionType
    let parameterType: ParameterType
    let value: String

    enum ParameterType {
        case label
        case value
    }

    enum ConditionType {
        case contains
    }
}
