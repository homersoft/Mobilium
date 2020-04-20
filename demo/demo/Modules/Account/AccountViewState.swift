//
//  AccountViewState.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Grzegorz Przybyła. All rights reserved.
//

import Foundation

enum AccountViewState {
    case initial
    case syncing
    case loaded([AccountField: Any])
    case error(title: String, message: String)
    case validationError(title: String, message: String)
    case saved
}
