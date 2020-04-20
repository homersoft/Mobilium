//
//  LoginViewState.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Silvair. All rights reserved.
//

import Foundation

enum LoginViewState {
    case initial
    case loaded(countires: [Country])
    case loading
    case error(title: String, text: String)
    case phoneNumberConfirmed
}
