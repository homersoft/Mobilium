//
//  Path.swift
//  MobiliumFramework
//
//  Created by Tomasz Oraczewski on 07/11/2019.
//  Copyright © 2019 Silvair. All rights reserved.
//

public struct Path: Equatable {
    public let elementType: ElementType
    public let condition: PathCondition?

    init(elementType: ElementType, condition: PathCondition? = nil) {
        self.elementType = elementType
        self.condition = condition
    }

    public enum ElementType {
        case cell
        case button
        case navigationBar
        case textField
        case textView
        case switchButton
    }
}

public struct PathCondition: Equatable {
    public let type: ConditionType
    public let parameterType: ParameterType
    public let value: String

    public enum ParameterType: String {
        case label
        case value
    }

    public enum ConditionType {
        case contains
    }
}
